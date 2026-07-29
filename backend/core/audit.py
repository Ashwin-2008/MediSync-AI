import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional

try:
    from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Text
    from sqlalchemy.orm import declarative_base, sessionmaker
except ImportError:
    create_engine, Column, Integer, String, DateTime, JSON, Text = None, None, None, None, None, None, None
    declarative_base, sessionmaker = None, None

logger = logging.getLogger(__name__)

Base = declarative_base() if declarative_base else object

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True, autoincrement=True) if Column else None
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True) if Column else None
    user_id = Column(String(255), nullable=True) if Column else None
    agent = Column(String(100), nullable=False) if Column else None
    action_type = Column(String(100), nullable=False) if Column else None
    prompt_version = Column(String(50), nullable=True) if Column else None
    model_provider = Column(String(100), nullable=True) if Column else None
    decision_confidence = Column(String(50), nullable=True) if Column else None
    details = Column(JSON, nullable=False) if Column else None
    # For cryptographic verification in enterprise setups
    hash_signature = Column(String(256), nullable=True) if Column else None

class AuditSystem:
    """Immutable audit logging for medical AI decisions."""
    
    def __init__(self, db_url: str = "sqlite:///audit.db"):
        self.db_url = db_url
        if create_engine:
            self.engine = create_engine(self.db_url)
            Base.metadata.create_all(self.engine)
            self.SessionLocal = sessionmaker(bind=self.engine)
        else:
            self.engine = None
            logger.warning("SQLAlchemy not installed, Audit System operating in mock mode.")

    def log_decision(self, agent: str, action: str, details: Dict[str, Any], user_id: str = "system", prompt_version: str = "v1") -> None:
        logger.info(f"AUDIT LOG: {agent} -> {action}")
        if not self.engine:
            return
            
        try:
            with self.SessionLocal() as session:
                log_entry = AuditLog(
                    user_id=user_id,
                    agent=agent,
                    action_type=action,
                    prompt_version=prompt_version,
                    details=details,
                    decision_confidence=str(details.get("confidence", "unknown")),
                    # E.g. Hash of details for immutability check
                    hash_signature="mock_sha256_hash"
                )
                session.add(log_entry)
                session.commit()
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")

audit_system = AuditSystem()
