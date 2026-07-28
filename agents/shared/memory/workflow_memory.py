from agents.shared.memory.cache import cache

class WorkflowMemory:
    @staticmethod
    def save_workflow_state(workflow_id: str, state: str, metadata: dict = None):
        data = {
            "current_state": state,
            "metadata": metadata or {}
        }
        cache.set(f"workflow:{workflow_id}", data, ex=86400 * 30)
        
    @staticmethod
    def get_workflow_state(workflow_id: str) -> dict:
        return cache.get(f"workflow:{workflow_id}") or {"current_state": "UNKNOWN", "metadata": {}}
