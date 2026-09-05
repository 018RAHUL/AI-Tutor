import json
import math
import re
import threading
import uuid
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Dict, Any
from backend.config import RAG_INDEX_PATH

class RAGRetriever:
    """Persistent lexical retriever with TF-IDF/BM25-style scoring.
    It survives process restarts and keeps document ownership metadata.
    """
    def __init__(self):
        self._lock = threading.RLock()
        self.documents: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        with self._lock:
            try:
                self.documents = json.loads(RAG_INDEX_PATH.read_text(encoding="utf-8"))
            except Exception:
                self.documents = []

    def _save(self):
        tmp = RAG_INDEX_PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.documents, ensure_ascii=False), encoding="utf-8")
        tmp.replace(RAG_INDEX_PATH)

    @staticmethod
    def _tokens(text):
        return re.findall(r"[a-zA-Z0-9_]+", text.lower())

    def add_documents(self, chunks: List[Dict[str, Any]], user_id: str = "legacy", source_filename: str = "unknown"):
        with self._lock:
            # Replace previous indexing of the same user's file.
            self.documents = [d for d in self.documents if not (d.get("user_id") == user_id and d.get("source_filename") == source_filename)]
            for chunk in chunks:
                content = chunk.get("content", "").strip()
                if not content: continue
                self.documents.append({"id": f"doc_{uuid.uuid4().hex}", "user_id": user_id, "source_filename": source_filename, "content": content, "metadata": chunk.get("metadata", {})})
            self._save()

    def search(self, query: str, user_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
        with self._lock:
            docs = [d for d in self.documents if d.get("user_id") == user_id]
        if not docs or not query.strip(): return []
        q = self._tokens(query)
        if not q: return []
        df = Counter()
        tokenized = {}
        for d in docs:
            t = self._tokens(d["content"]); tokenized[d["id"]] = t
            df.update(set(t))
        avgdl = sum(len(v) for v in tokenized.values()) / max(len(tokenized), 1)
        k1, b = 1.5, 0.75
        scored=[]
        for d in docs:
            tokens=tokenized[d["id"]]; counts=Counter(tokens); dl=len(tokens); score=0.0
            for term in q:
                if not counts[term]: continue
                idf=math.log(1 + (len(docs)-df[term]+0.5)/(df[term]+0.5))
                tf=counts[term]
                score += idf * (tf*(k1+1))/(tf+k1*(1-b+b*dl/max(avgdl,1)))
            if score>0: scored.append((score,d))
        scored.sort(key=lambda x:x[0], reverse=True)
        return [{**d, "score": round(score,4)} for score,d in scored[:top_k]]

    def retrieve(self, query: str, top_k: int = 5, user_id: str = "legacy") -> List[Dict[str, Any]]:
        return self.search(query=query, user_id=user_id, top_k=top_k)
