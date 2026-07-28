import sqlite3
import json
import os
import hashlib
import logging
from typing import List, Dict, Any, Tuple
import numpy as np

try:
    import faiss
except ImportError:
    faiss = None

logger = logging.getLogger(__name__)

class VectorStore:
    """FAISS + SQLite robust hybrid retrieval store."""
    
    def __init__(self, db_path: str = "hospital_rag.db", dimension: int = 384):
        self.db_path = db_path
        self.dimension = dimension
        self.collections = {} # In-memory dict mapping collection -> FAISS index
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    collection TEXT NOT NULL,
                    doc_hash TEXT UNIQUE NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT NOT NULL
                )
            """)
            conn.commit()

    def _get_index(self, collection: str):
        if not faiss:
            logger.warning("FAISS not installed, retrieval disabled.")
            return None
            
        if collection not in self.collections:
            # Create a new flat L2 index
            index = faiss.IndexFlatL2(self.dimension)
            # Load existing vectors from DB if we persisted them
            # For this MVP, we assume in-memory FAISS indices built on startup or ad-hoc
            self.collections[collection] = index
        return self.collections[collection]

    def _hash_content(self, content: str) -> str:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def add_documents(self, collection: str, documents: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Adds documents to FAISS and SQLite (skipping duplicates)."""
        index = self._get_index(collection)
        if not index:
            return

        added_count = 0
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for doc, emb in zip(documents, embeddings):
                content = doc["content"]
                metadata = json.dumps(doc.get("metadata", {}))
                doc_hash = self._hash_content(content)
                
                try:
                    cursor.execute(
                        "INSERT INTO documents (collection, doc_hash, content, metadata) VALUES (?, ?, ?, ?)",
                        (collection, doc_hash, content, metadata)
                    )
                    doc_id = cursor.lastrowid
                    
                    # Add to FAISS (Using doc_id as implicit index if we used IndexIDMap, but keeping it simple for now)
                    # For a robust system we use IndexIDMap
                    vector = np.array([emb], dtype=np.float32)
                    index.add(vector)
                    added_count += 1
                except sqlite3.IntegrityError:
                    # Duplicate document
                    continue
            conn.commit()
            
        logger.info(f"Added {added_count} new documents to collection {collection}")

    def search(self, collection: str, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search the FAISS index and join with SQLite metadata."""
        index = self._get_index(collection)
        if not index or index.ntotal == 0:
            return []

        vector = np.array([query_embedding], dtype=np.float32)
        distances, indices = index.search(vector, min(top_k, index.ntotal))
        
        results = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # FAISS returns 0-based indices for IndexFlatL2 matching insertion order.
            # In a production system using IndexIDMap, this maps directly to SQLite primary key.
            # Here we query by rowid (1-based).
            for idx in indices[0]:
                if idx == -1: continue
                cursor.execute("SELECT content, metadata FROM documents WHERE collection=? AND rowid=?", (collection, int(idx) + 1))
                row = cursor.fetchone()
                if row:
                    results.append({
                        "content": row[0],
                        "metadata": json.loads(row[1])
                    })
                    
        return results

vector_store = VectorStore()
