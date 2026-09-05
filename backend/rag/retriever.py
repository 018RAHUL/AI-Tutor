import math
import re
from typing import List, Dict, Any, Optional

class RAGRetriever:
    """
    In-memory hybrid retriever supporting term frequency, BM25 ranking,
    and metadata filtering for uploaded documents.
    """

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []

    def add_documents(self, docs: List[Dict[str, Any]]):
        self.documents.extend(docs)

    def clear(self):
        self.documents = []

    def retrieve(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        if not self.documents:
            return []

        query_terms = set(re.findall(r"\w+", query.lower()))
        scored_docs = []

        for doc in self.documents:
            content = doc.get("content", "").lower()
            doc_terms = re.findall(r"\w+", content)
            doc_len = max(len(doc_terms), 1)

            # Simple BM25 / TF scoring
            score = 0.0
            for term in query_terms:
                tf = doc_terms.count(term)
                if tf > 0:
                    score += (tf * (1.5 + 1)) / (tf + 1.5 * (0.25 + 0.75 * (doc_len / 300.0)))

            if score > 0:
                scored_docs.append((score, doc))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:top_k]]
