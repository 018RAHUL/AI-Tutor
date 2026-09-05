import re
from pathlib import Path
from typing import List, Dict, Any

class DocumentParser:
    @classmethod
    def parse(cls, file_path: str) -> List[Dict[str, Any]]:
        path=Path(file_path)
        if path.suffix.lower()==".pdf": return cls.parse_pdf(file_path)
        text=path.read_text(encoding="utf-8", errors="ignore")
        clean=cls.clean_text(text)
        return [{"content": c, "metadata": {"source": path.name, "page": 1, "chunk_id": f"c_{i+1}"}} for i,c in enumerate(cls.chunk_text(clean))]

    @classmethod
    def parse_pdf(cls, file_path: str) -> List[Dict[str, Any]]:
        import pypdf
        chunks=[]
        reader=pypdf.PdfReader(file_path)
        for page_idx,page in enumerate(reader.pages):
            clean=cls.clean_text(page.extract_text() or "")
            for i,c in enumerate(cls.chunk_text(clean)):
                chunks.append({"content":c,"metadata":{"source":Path(file_path).name,"page":page_idx+1,"chunk_id":f"p{page_idx+1}_c{i+1}"}})
        return chunks

    @staticmethod
    def clean_text(text: str)->str:
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def chunk_text(text: str, chunk_size: int=450, overlap: int=75)->List[str]:
        words=text.split();
        if not words: return []
        chunks=[]; start=0
        while start<len(words):
            end=min(start+chunk_size,len(words)); chunks.append(" ".join(words[start:end]))
            if end==len(words): break
            start=end-overlap
        return chunks
