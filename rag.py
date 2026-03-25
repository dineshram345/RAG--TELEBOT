import os
import sqlite3
import glob
import numpy as np
from sentence_transformers import SentenceTransformer
import ollama

"""
Mini-RAG core:
- read docs from ./docs
- split into overlapping word chunks
- embed with SentenceTransformers
- store embeddings in SQLite (BLOB)
- retrieve by cosine similarity
- call Ollama to generate an answer from retrieved context
"""

EMBED_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "phi3"
DB_PATH = "vectors.db"
DOCS_DIR = "docs"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
TOP_K = 3

_embedder = None


def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder


# --- Chunking ---

def load_documents(docs_dir=DOCS_DIR):
    docs = []
    files = glob.glob(os.path.join(docs_dir, "*.md")) + glob.glob(os.path.join(docs_dir, "*.txt"))
    for filepath in sorted(files):
        with open(filepath, "r") as f:
            text = f.read()
        source = os.path.basename(filepath)
        docs.append((source, text))
    return docs


def split_into_chunks(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    if overlap >= chunk_size:
        raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")

    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


# --- SQLite Vector Store ---

def init_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            text TEXT,
            embedding BLOB
        )
    """
    )
    conn.commit()
    return conn


def store_chunks(chunks_with_source, embeddings, db_path=DB_PATH):
    conn = init_db(db_path)
    try:
        for (source, text), emb in zip(chunks_with_source, embeddings):
            emb_bytes = np.array(emb, dtype=np.float32).tobytes()
            conn.execute(
                "INSERT INTO chunks (source, text, embedding) VALUES (?, ?, ?)",
                (source, text, emb_bytes),
            )
        conn.commit()
    finally:
        conn.close()


def search(query_embedding, top_k=TOP_K, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute("SELECT id, source, text, embedding FROM chunks").fetchall()
    finally:
        conn.close()

    if not rows:
        return []

    query_vec = np.array(query_embedding, dtype=np.float32)
    query_norm = np.linalg.norm(query_vec)

    scored = []
    for row_id, source, text, emb_bytes in rows:
        stored_vec = np.frombuffer(emb_bytes, dtype=np.float32)
        score = np.dot(query_vec, stored_vec) / (query_norm * np.linalg.norm(stored_vec) + 1e-10)
        scored.append((score, source, text))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]


# --- Ingestion ---

def ingest(docs_dir=DOCS_DIR, db_path=DB_PATH):
    if os.path.exists(db_path):
        os.remove(db_path)

    documents = load_documents(docs_dir)
    if not documents:
        print("No documents found in", docs_dir)
        return

    all_chunks = []
    for source, text in documents:
        chunks = split_into_chunks(text)
        for chunk in chunks:
            all_chunks.append((source, chunk))

    print(f"Loaded {len(documents)} docs, split into {len(all_chunks)} chunks")

    model = get_embedder()
    texts = [text for _, text in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True)

    store_chunks(all_chunks, embeddings, db_path)
    print(f"Stored {len(all_chunks)} chunks in {db_path}")


# --- RAG Pipeline ---

def ask(question):
    model = get_embedder()
    query_embedding = model.encode(question)

    results = search(query_embedding)
    if not results:
        return "No documents found. Please run ingest.py first."

    context_parts = []
    sources = set()
    for score, source, text in results:
        context_parts.append(text)
        sources.add(source)

    context = "\n\n".join(context_parts)

    prompt = f"""Use the following context to answer the question. If the context doesn't contain enough information, say so honestly. Keep the answer concise.

Context:
{context}

Question: {question}

Answer:"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    answer = response["message"]["content"]

    source_list = ", ".join(sorted(sources))
    return f"{answer}\n\nSources: {source_list}"
