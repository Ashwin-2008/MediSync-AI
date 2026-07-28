import re
import logging
from typing import List, Dict, Any

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

logger = logging.getLogger(__name__)

class SemanticChunker:
    """Chunks text based on sentences and paragraphs while respecting a max token limit."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[str]:
        """Simple regex-based sentence splitter for chunking."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            # Approximate token length (words)
            length = len(sentence.split())
            if current_length + length > self.chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                # Keep overlap (approx last 1-2 sentences)
                overlap_size = 0
                overlap_chunk = []
                for s in reversed(current_chunk):
                    if overlap_size + len(s.split()) <= self.chunk_overlap:
                        overlap_chunk.insert(0, s)
                        overlap_size += len(s.split())
                    else:
                        break
                current_chunk = overlap_chunk
                current_length = overlap_size
            
            current_chunk.append(sentence)
            current_length += length
            
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks

class EmbeddingEngine:
    """Generates dense vector embeddings for RAG."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = None
        if SentenceTransformer:
            logger.info(f"Loading embedding model: {model_name}")
            try:
                self.model = SentenceTransformer(model_name)
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
        else:
            logger.warning("sentence-transformers not installed. Using mock embeddings.")

    def generate_embedding(self, text: str) -> List[float]:
        """Generates a vector embedding for a single text chunk."""
        if self.model:
            return self.model.encode(text).tolist()
        # Mock embedding (384 dimensions matching MiniLM)
        return [0.1] * 384
        
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        if self.model:
            return self.model.encode(texts).tolist()
        return [[0.1] * 384 for _ in texts]
