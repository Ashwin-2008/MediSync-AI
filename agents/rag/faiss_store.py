import sqlite3
import json
import logging
from typing import List, Dict, Any
from agents.rag.vector_store_interface import VectorStore
# import faiss
# import numpy as np

logger = logging.getLogger(__name__)

class FaissSQLiteStore(VectorStore):
    def __init__(self, db_path: str = "agents/rag/metadata.db", dimension: int = 768):
        self.db_path = db_path
        self.dimension = dimension
        # self.index = faiss.IndexFlatL2(dimension)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS metadata
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      text TEXT,
                      metadata_json TEXT)''')
        conn.commit()
        conn.close()

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]]) -> None:
        # Mocking embeddings generation
        # embeddings = generate_embeddings(texts)
        # self.index.add(np.array(embeddings).astype('float32'))
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        for text, meta in zip(texts, metadatas):
            c.execute("INSERT INTO metadata (text, metadata_json) VALUES (?, ?)", 
                      (text, json.dumps(meta)))
        conn.commit()
        conn.close()
        logger.info(f"Added {len(texts)} documents to FAISS+SQLite store.")

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        # Mocking search
        # query_embedding = generate_embeddings([query])[0]
        # distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), k)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Mock returning the first k rows
        c.execute("SELECT text, metadata_json FROM metadata LIMIT ?", (k,))
        results = [{"text": row[0], "metadata": json.loads(row[1])} for row in c.fetchall()]
        conn.close()
        return results
