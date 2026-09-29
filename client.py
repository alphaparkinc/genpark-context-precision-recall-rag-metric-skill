"""RAG Context Precision & Recall Evaluator.
100% Python Standard Library.
"""

class RAGContextEvaluator:
    """Computes Mean Average Precision (MAP) and Recall for retrieved RAG contexts."""
    @staticmethod
    def evaluate(retrieved_chunks, relevant_chunks):
        rel_set = set(relevant_chunks)
        hits = 0
        precisions = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            if chunk in rel_set:
                hits += 1
                precisions.append(hits / i)
        avg_precision = sum(precisions) / max(len(rel_set), 1)
        recall = hits / max(len(rel_set), 1)
        return {
            "context_precision": round(avg_precision, 4),
            "context_recall": round(recall, 4),
            "hits": hits
        }
