# app/generation/generator.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.5-flash"

SYSTEM_PROMPT = """You are a helpful assistant that answers questions using ONLY the provided context.
If the answer isn't in the context, say you don't know — do not make things up.
Always cite which source(s) you used, referencing the source filename given in the context."""

def build_prompt(query: str, retrieved_chunks: list[str], sources: list[str]) -> str:
    context_blocks = []
    for chunk, source in zip(retrieved_chunks, sources):
        context_blocks.append(f"[Source: {source}]\n{chunk}")
    context_text = "\n\n---\n\n".join(context_blocks)

    prompt = f"""{SYSTEM_PROMPT}

Context:
{context_text}

Question: {query}

Answer (with source citations):"""
    return prompt

def generate_answer(query: str, retrieved_chunks: list[str], sources: list[str]) -> str:
    prompt = build_prompt(query, retrieved_chunks, sources)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    from app.embeddings.store import get_chroma_collection, query_collection

    collection = get_chroma_collection()
    query = "What programming languages does this candidate know?"
    results = query_collection(collection, query)

    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    sources = [m["source"] for m in metadatas]

    answer = generate_answer(query, chunks, sources)
    print("\n=== ANSWER ===\n")
    print(answer)