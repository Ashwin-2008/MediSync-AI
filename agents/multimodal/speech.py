import logging
from typing import Dict, Any

try:
    import whisper
except ImportError:
    whisper = None

logger = logging.getLogger(__name__)

class SpeechProcessor:
    """Processes audio to text using OpenAI Whisper."""
    
    def __init__(self, model_size: str = "tiny"):
        self.model = None
        if whisper:
            try:
                self.model = whisper.load_model(model_size)
                logger.info(f"Loaded Whisper model: {model_size}")
            except Exception as e:
                logger.error(f"Failed to load Whisper model: {e}")
        else:
            logger.warning("Whisper is not installed.")
            
    def process(self, file_path: str) -> Dict[str, Any]:
        if not self.model:
            return {"text": "[MOCK AUDIO TRANSCRIPT] Patient reports chest pain.", "confidence": 0.0}
            
        try:
            result = self.model.transcribe(file_path)
            return {
                "text": result["text"].strip(),
                "language": result.get("language", "unknown"),
                "source": file_path
            }
        except Exception as e:
            logger.error(f"Speech processing failed: {e}")
            return {"error": str(e)}

# Singleton instance for app lifetime
speech_processor = SpeechProcessor()
