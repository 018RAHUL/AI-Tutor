import pytest
from backend.rag.parser import DocumentParser
from backend.rag.retriever import RAGRetriever

def test_document_parser_clean_and_chunk():
    text = "Ohm's Law states that the current through a conductor between two points is directly proportional to the voltage across the two points. Introducing the constant of proportionality, the resistance, one arrives at the usual mathematical equation that describes this relationship: V = I * R."
    chunks = DocumentParser.chunk_text(text, chunk_size=20, overlap=5)
    assert len(chunks) >= 1
    assert "Ohm's Law" in chunks[0]

def test_rag_retriever():
    retriever = RAGRetriever()
    docs = [
        {"content": "Voltage is the difference in electric potential between two points.", "metadata": {"source": "physics.pdf", "page": 1}},
        {"content": "Binary search is an efficient algorithm for finding an item from a sorted list.", "metadata": {"source": "algorithms.pdf", "page": 1}}
    ]
    retriever.add_documents(docs)
    
    results = retriever.retrieve("electric potential voltage")
    assert len(results) >= 1
    assert "Voltage" in results[0]["content"]
