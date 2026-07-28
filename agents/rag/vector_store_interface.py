from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorStore(ABC):
    @abstractmethod
    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]]) -> None:
        pass

    @abstractmethod
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        pass
