from agents.shared.memory.cache import cache
import uuid

class SessionManager:
    @staticmethod
    def create_session(user_id: str, role: str) -> str:
        session_id = str(uuid.uuid4())
        session_data = {
            "user_id": user_id,
            "role": role,
            "active": True
        }
        cache.set(f"session:{session_id}", session_data, ex=86400) # 24h expiration
        return session_id
        
    @staticmethod
    def get_session(session_id: str) -> dict:
        return cache.get(f"session:{session_id}")

    @staticmethod
    def invalidate_session(session_id: str):
        cache.delete(f"session:{session_id}")
