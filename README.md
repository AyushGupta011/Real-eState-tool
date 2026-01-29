# Real Estate Research Tool

An AI-powered research assistant that scrapes real estate and financial pages, indexes them into a local vector store, and answers context-aware questions using Groq's Llama models.

## Features
- URL scraping: Extracts text from web pages using `unstructured`.
- Vector storage: Uses ChromaDB for local embeddings and persistence.
- Embeddings: Uses the `thenlper/gte-base` embedding model for semantic search.
- LLM answering: Uses Groq/ChatGroq (Llama) for responses with contextual retrieval.
- Streamlit frontend: Simple UI to process URLs and chat with indexed documents.

## Quick Start
1. Create and activate a virtual environment (recommended):

```
python -m venv .venv
```

On Windows:

```
.venv\Scripts\activate
```

On macOS / Linux:

```
source .venv/bin/activate
```

2. Install dependencies:

```
pip install -r requirements.txt
```

Or install the full stack:

```
pip install streamlit langchain langchain-community langchain-huggingface langchain-chroma langchain-groq unstructured python-dotenv sentence-transformers
```

Note (Windows): if `unstructured` reports file-type or libmagic issues, run:
```
pip install python-magic-bin
```


## Configuration
1. Create a `.env` file in the project root with your Groq API key:

```
 GROQ_API_KEY=your_groq_api_key_here
  ```




## Project Structure

The expected layout for the minimal app:

- `real_state_tool/`
	- `main.py` or `app.py` — Streamlit frontend
	- `rag.py` — RAG processing & indexing code
	- `requirements.txt`
	- `resources/` — ChromaDB persistence (created at runtime)


## Usage
Run the Streamlit app:

```
streamlit run app.py
```

Workflow:
- Enter up to 3 URLs in the sidebar.
- Click **Process URLs** to scrape, split, embed, and index content.
- Ask questions in the chat — the app retrieves relevant context and uses the LLM to answer.


## Requirements
Add these to `requirements.txt` (example):

```
streamlit
langchain
langchain-community
langchain-huggingface
langchain-chroma
langchain-groq
unstructured
python-dotenv
sentence-transformers

```


## Notes & Tips
- First run may download the `gte-base` embedding model (~200MB).
- Indexed data persists under `resources/`; you can reuse it instead of re-processing URLs.
- If you need robust HTML scraping, consider adding `beautifulsoup4` or `trafilatura` as optional helpers.
