import os
import re
from pathlib import Path
from typing import List, Dict, Any

class DocumentParser:
    """
    Parses PDF, Markdown, and text files into clean structured chunks with metadata.
    """

    @classmethod
    def parse_pdf(cls, file_path: str) -> List[Dict[str, Any]]:
        chunks = []
        try:
            import pypdf
            reader = pypdf.PdfReader(file_path)
            for page_idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                clean_text = cls.clean_text(text)
                if clean_text:
                    sub_chunks = cls.chunk_text(clean_text, chunk_size=500, overlap=80)
                    for chunk_idx, chunk in enumerate(sub_chunks):
                        chunks.append({
                            "content": chunk,
                            "metadata": {
                                "source": Path(file_path).name,
                                "page": page_idx + 1,
                                "chunk_id": f"p{page_idx + 1}_c{chunk_idx + 1}"
                            }
                        })
        except Exception as e:
            print(f"[DocumentParser] PDF parsing error: {e}")
            # Fallback to raw text read if not binary PDF
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                clean = cls.clean_text(text)
                sub_chunks = cls.chunk_text(clean, chunk_size=500, overlap=80)
                for i, c in enumerate(sub_chunks):
                    chunks.append({"content": c, "metadata": {"source": Path(file_path).name, "page": 1, "chunk_id": f"c_{i}"}})
            except Exception:
                pass
        return chunks

    @classmethod
    def clean_text(cls, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    @classmethod
    def chunk_text(cls, text: str, chunk_size: int = 500, overlap: int = 80) -> List[str]:
        words = text.split()
        if len(words) <= chunk_size:
            return [text]
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk_str = " ".join(words[start:end])
            chunks.append(chunk_str)
            if end >= len(words):
                break
            start += (chunk_size - overlap)
        return chunks
