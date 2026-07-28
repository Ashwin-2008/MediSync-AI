from agents.shared.memory.cache import cache

class PatientMemory:
    @staticmethod
    def save_patient_state(patient_id: str, state: dict):
        cache.set(f"patient_state:{patient_id}", state, ex=86400 * 7) # 7 days
        
    @staticmethod
    def get_patient_state(patient_id: str) -> dict:
        return cache.get(f"patient_state:{patient_id}") or {}
        
    @staticmethod
    def update_patient_state(patient_id: str, updates: dict):
        state = PatientMemory.get_patient_state(patient_id)
        state.update(updates)
        PatientMemory.save_patient_state(patient_id, state)
