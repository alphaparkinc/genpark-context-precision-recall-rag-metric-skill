from client import RAGContextEvaluator

retrieved = ["doc_A", "doc_B", "doc_C"]
golden = ["doc_A", "doc_C"]

scores = RAGContextEvaluator.evaluate(retrieved, golden)
print("RAG Metric Evaluation:", scores)
