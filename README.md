# Enterprise RAG Knowledge Assistant

An AI-powered assistant that ingests documents (PDFs, policies, technical files) and answers questions about them using Retrieval-Augmented Generation (RAG). Built with a full RAG pipeline: document ingestion, chunking, embeddings, vector search, and LLM-based answer generation with source citations.

## Features

- **PDF ingestion** — extracts text from PDF documents
- **Chunking** — splits documents into overlapping chunks for better retrieval
- **Embeddings** — converts text chunks into vector embeddings using Sentence Transformers
- **Vector database** — stores and searches embeddings using ChromaDB
- **Semantic search** — retrieves the most relevant chunks for a given question
- **LLM answer generation** — uses Google Gemini to generate grounded answers
- **Source citations** — every answer references which document it came from
- **Interactive CLI chat** — ask multiple questions in a live terminal session

## Tech Stack

- **Language:** Python 3.11
- **LLM:** Google Gemini (`gemini-3.5-flash`)
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Vector Database:** ChromaDB
- **Document Parsing:** PyPDF
- **Chunking:** LangChain Text Splitters
- **Database (planned):** PostgreSQL (via Docker) for chat history/metadata

## Project Structure


Enterprise_RAG_knowledge_Assistant/
├── app/
│ ├── ingestion/ # PDF loading and text chunking
│ │ ├── loader.py
│ │ └── chunker.py
│ ├── embeddings/ # Embedding generation and vector store
│ │ └── store.py
│ ├── generation/ # LLM prompt building and answer generation
│ │ └── generator.py
│ └── api/ # Interactive chat interface
│ └── cli_chat.py
├── data/
│ ├── raw/ # Source PDF documents
│ └── processed/ # ChromaDB persistent storage (gitignored)
├── requirements.txt
├── docker-compose.yml
└── .env # API keys (gitignored, not committed)





## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/archit335/enterprise-rag-knowledge-assistant.git
cd enterprise-rag-knowledge-assistant
```

### 2. Create a virtual environment

```bash
python3.11 -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Create a `.env` file in the project root:




GEMINI_API_KEY=your-gemini-api-key-here

Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey).

### 5. Add your documents

Place any PDF files you want the assistant to learn from into `data/raw/`:

```bash
cp /path/to/your/document.pdf data/raw/
```

### 6. Run the assistant

```bash
python -m app.api.cli_chat
```

Ask questions about your documents directly in the terminal. Type `exit` to quit.

## Example Usage
=== Enterprise RAG Knowledge Assistant ===
Type your question, or 'exit' to quit.

You: What projects has this candidate worked on?

Assistant: Based on the provided resume, the candidate has worked on...
Source: your_document.pdf

## How It Works

1. **Ingestion** — PDFs in `data/raw/` are loaded and text is extracted page by page.
2. **Chunking** — Extracted text is split into overlapping ~800-character chunks to preserve context.
3. **Embedding** — Each chunk is converted into a vector embedding using a local Sentence Transformer model.
4. **Storage** — Embeddings are stored in a local ChromaDB vector database.
5. **Retrieval** — When a question is asked, it's embedded and compared against stored chunks to find the most relevant ones.
6. **Generation** — Retrieved chunks are passed to Gemini as context, which generates a grounded answer with source citations.

## Roadmap

- [ ] Hybrid search (keyword + semantic)
- [ ] Reranking of retrieved chunks
- [ ] Multi-turn conversation memory
- [ ] PostgreSQL integration for chat history
- [ ] RAG evaluation pipeline (RAGAS)
- [ ] REST API (FastAPI) for external integrations
- [ ] Support for more file types (docx, txt, markdown)

## Author

**Archit Kumar Singh**
[LinkedIn](https://linkedin.com/in/archit-kumar---singh) • [GitHub](https://github.com/archit335)