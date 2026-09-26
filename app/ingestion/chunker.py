# app/ingestion/chunker.py
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text: str, chunk_size: int = 800, chunk_overlap: int = 150) -> list[str]:
    """Split text into overlapping chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)

if __name__ == "__main__":
    from app.ingestion.loader import load_all_pdfs

    docs = load_all_pdfs("data/raw")
    for name, text in docs.items():
        chunks = chunk_text(text)
        print(f"\n{name}: {len(chunks)} chunks")
        print("First chunk preview:\n", chunks[0][:300])