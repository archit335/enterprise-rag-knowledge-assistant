# app/embeddings/store.py
import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = "data/processed/chroma_db"
COLLECTION_NAME = "documents"

def get_chroma_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn,
    )
    return collection

def add_chunks(collection, chunks: list[str], source_name: str):
    ids = [f"{source_name}_{i}" for i in range(len(chunks))]
    metadatas = [{"source": source_name, "chunk_index": i} for i in range(len(chunks))]
    collection.add(documents=chunks, ids=ids, metadatas=metadatas)

def query_collection(collection, query: str, n_results: int = 5):
    results = collection.query(query_texts=[query], n_results=n_results)
    return results

if __name__ == "__main__":
    from app.ingestion.loader import load_all_pdfs
    from app.ingestion.chunker import chunk_text

    collection = get_chroma_collection()
    docs = load_all_pdfs("data/raw")

    for name, text in docs.items():
        chunks = chunk_text(text)
        add_chunks(collection, chunks, source_name=name)
        print(f"Added {len(chunks)} chunks from {name}")

    test_query = "What is this candidate's experience?"
    results = query_collection(collection, test_query)
    print("\n--- Query results ---")
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"[{meta['source']} chunk {meta['chunk_index']}]: {doc[:150]}...")