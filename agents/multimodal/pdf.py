import logging
from typing import Dict, Any

try:
    import fitz # PyMuPDF
except ImportError:
    fitz = None

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Extracts text and metadata from PDF files."""
    
    @staticmethod
    def process(file_path: str) -> Dict[str, Any]:
        if not fitz:
            logger.warning("PyMuPDF not installed.")
            return {"text": "[MOCK PDF CONTENT] Lab results normal.", "pages": 0}
            
        try:
            doc = fitz.open(file_path)
            full_text = []
            for page in doc:
                full_text.append(page.get_text("text"))
            return {
                "text": "\n".join(full_text).strip(),
                "pages": len(doc),
                "metadata": doc.metadata
            }
        except Exception as e:
            logger.error(f"PDF processing failed: {e}")
            return {"error": str(e)}
