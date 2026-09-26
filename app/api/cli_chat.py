# app/api/cli_chat.py
from app.embeddings.store import get_chroma_collection, query_collection
from app.generation.generator import generate_answer

def main():
    print("=== Enterprise RAG Knowledge Assistant ===")
    print("Type your question, or 'exit' to quit.\n")

    collection = get_chroma_collection()

    while True:
        query = input("You: ").strip()
        if query.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not query:
            continue

        results = query_collection(collection, query, n_results=5)
        chunks = results["documents"][0]
        metadatas = results["metadatas"][0]
        sources = [m["source"] for m in metadatas]

        if not chunks:
            print("Assistant: I couldn't find anything relevant in the documents.\n")
            continue

        answer = generate_answer(query, chunks, sources)
        print(f"\nAssistant: {answer}\n")

if __name__ == "__main__":
    main()