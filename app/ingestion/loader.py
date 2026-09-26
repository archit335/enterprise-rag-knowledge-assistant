# app/ingestion/loader.py
import os
from pypdf import PdfReader

def load_pdf(file_path: str) -> str:
    """Extract raw text from a single PDF file."""
    reader = PdfReader(file_path)
    text = ""
    for page_num, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text += f"\n\n[Page {page_num + 1}]\n{page_text}"
    return text

def load_all_pdfs(folder_path: str) -> dict:
    """Load all PDFs in a folder. Returns {filename: text}."""
    docs = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            print(f"Loading: {filename}")
            docs[filename] = load_pdf(full_path)
    return docs

if __name__ == "__main__":
    docs = load_all_pdfs("data/raw")
    for name, text in docs.items():
        print(f"\n--- {name} ---")
        print(text[:500])