import sys
import json
from client import RAGContextEvaluator

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-context-precision-recall-rag-metric-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_rag_context",
                        "description": "Evaluate context precision and recall for retrieved chunk list",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "retrieved_chunks": {"type": "array", "items": {"type": "string"}},
                                "relevant_chunks": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["retrieved_chunks", "relevant_chunks"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        args = params.get("arguments", {})
        ret = args.get("retrieved_chunks", [])
        rel = args.get("relevant_chunks", [])
        res = RAGContextEvaluator.evaluate(ret, rel)
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
