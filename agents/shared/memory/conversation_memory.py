from agents.shared.memory.cache import cache
from typing import List, Dict

class ConversationMemory:
    @staticmethod
    def add_message(session_id: str, role: str, content: str):
        key = f"conv_history:{session_id}"
        history = cache.get(key) or []
        history.append({"role": role, "content": content})
        cache.set(key, history, ex=86400 * 3) # 3 days
        
    @staticmethod
    def get_history(session_id: str, limit: int = 50) -> List[Dict[str, str]]:
        history = cache.get(f"conv_history:{session_id}") or []
        return history[-limit:]
