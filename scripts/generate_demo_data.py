import random
import logging
from typing import List, Dict

try:
    from faker import Faker
    import sqlite3
except ImportError:
    Faker, sqlite3 = None, None

logger = logging.getLogger(__name__)

class DemoDataGenerator:
    """Generates thousands of synthetic medical records for demonstration."""
    
    def __init__(self, db_path: str = "hospital_demo.db"):
        self.db_path = db_path
        self.fake = Faker()
        
    def _init_db(self):
        if not sqlite3: return
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    dob TEXT,
                    gender TEXT,
                    blood_type TEXT
                )
            """)
            conn.commit()
            
    def generate_patients(self, count: int = 1000):
        if not sqlite3 or not self.fake:
            logger.warning("Faker or sqlite3 not installed. Skipping data generation.")
            return
            
        self._init_db()
        logger.info(f"Generating {count} synthetic patients...")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for _ in range(count):
                pt_id = f"PT-{self.fake.random_int(min=10000, max=99999)}"
                name = self.fake.name()
                dob = self.fake.date_of_birth(minimum_age=1, maximum_age=90).isoformat()
                gender = random.choice(["Male", "Female"])
                blood_type = random.choice(["A+", "O+", "B+", "AB+", "O-"])
                
                try:
                    cursor.execute(
                        "INSERT INTO patients (id, name, dob, gender, blood_type) VALUES (?, ?, ?, ?, ?)",
                        (pt_id, name, dob, gender, blood_type)
                    )
                except sqlite3.IntegrityError:
                    pass
            conn.commit()
        logger.info("Demo patient generation complete.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generator = DemoDataGenerator()
    generator.generate_patients(1000)
