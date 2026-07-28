import re
import logging
from typing import Dict, Any

try:
    from cryptography.fernet import Fernet
except ImportError:
    Fernet = None

logger = logging.getLogger(__name__)

class SecurityCore:
    """Core security utilities including encryption, injection detection, and masking."""
    
    def __init__(self):
        # In production this comes from secrets manager
        self._key = Fernet.generate_key() if Fernet else None
        self._cipher = Fernet(self._key) if Fernet else None

    def encrypt_phi(self, data: str) -> str:
        """Encrypts Protected Health Information (PHI) at rest."""
        if not self._cipher:
            return data
        return self._cipher.encrypt(data.encode()).decode()

    def decrypt_phi(self, encrypted_data: str) -> str:
        if not self._cipher:
            return encrypted_data
        try:
            return self._cipher.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return "<DECRYPTION_ERROR>"

    def detect_prompt_injection(self, user_input: str) -> bool:
        """Heuristic detection of common prompt injection vectors."""
        # Highly simplified for demo purposes
        injection_patterns = [
            r"ignore previous instructions",
            r"system prompt",
            r"you are now",
            r"bypass rules",
            r"output exactly"
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                logger.warning(f"SECURITY: Potential prompt injection detected: {pattern}")
                return True
        return False

    def mask_sensitive_data(self, text: str) -> str:
        """Masks SSNs and other PII in logs."""
        # Mask SSN (XXX-XX-XXXX)
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', 'XXX-XX-XXXX', text)
        # Mask simple credit cards
        text = re.sub(r'\b(?:\d[ -]*?){13,16}\b', 'XXXX-XXXX-XXXX-XXXX', text)
        return text

security_core = SecurityCore()
