import os
import csv
import logging
from typing import List, Dict, Any
from abc import ABC, abstractmethod

# Stubs for heavy dependencies to allow graceful failure if not installed
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None
    Image = None

try:
    import docx
except ImportError:
    docx = None

logger = logging.getLogger(__name__)

class DocumentLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> List[Dict[str, Any]]:
        """Returns a list of chunks/pages with metadata."""
        pass

class PDFLoader(DocumentLoader):
    def load(self, file_path: str) -> List[Dict[str, Any]]:
        if not fitz:
            logger.error("PyMuPDF (fitz) is not installed.")
            return []
        
        documents = []
        try:
            doc = fitz.open(file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text("text")
                if text.strip():
                    documents.append({
                        "content": text,
                        "metadata": {
                            "source": file_path,
                            "page": page_num + 1,
                            "type": "pdf"
                        }
                    })
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {e}")
        return documents

class OCRLoader(DocumentLoader):
    def load(self, file_path: str) -> List[Dict[str, Any]]:
        if not pytesseract or not Image:
            logger.error("pytesseract or PIL is not installed.")
            return []
            
        try:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)
            return [{
                "content": text,
                "metadata": {
                    "source": file_path,
                    "type": "ocr_image"
                }
            }]
        except Exception as e:
            logger.error(f"Error OCR loading {file_path}: {e}")
            return []

class CSVLoader(DocumentLoader):
    def load(self, file_path: str) -> List[Dict[str, Any]]:
        documents = []
        try:
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row_idx, row in enumerate(reader):
                    # Convert row to string representation
                    content = " | ".join([f"{k}: {v}" for k, v in row.items()])
                    documents.append({
                        "content": content,
                        "metadata": {
                            "source": file_path,
                            "row": row_idx,
                            "type": "csv"
                        }
                    })
        except Exception as e:
            logger.error(f"Error loading CSV {file_path}: {e}")
        return documents

class DOCXLoader(DocumentLoader):
    def load(self, file_path: str) -> List[Dict[str, Any]]:
        if not docx:
            logger.error("python-docx is not installed.")
            return []
            
        documents = []
        try:
            doc = docx.Document(file_path)
            full_text = [para.text for para in doc.paragraphs if para.text.strip()]
            documents.append({
                "content": "\n".join(full_text),
                "metadata": {
                    "source": file_path,
                    "type": "docx"
                }
            })
        except Exception as e:
            logger.error(f"Error loading DOCX {file_path}: {e}")
        return documents

class TXTLoader(DocumentLoader):
    def load(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return [{
                    "content": f.read(),
                    "metadata": {
                        "source": file_path,
                        "type": "txt"
                    }
                }]
        except Exception as e:
            logger.error(f"Error loading TXT {file_path}: {e}")
            return []

class UniversalLoader:
    """Factory to pick the right loader."""
    @staticmethod
    def load_file(file_path: str) -> List[Dict[str, Any]]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return PDFLoader().load(file_path)
        elif ext in ['.png', '.jpg', '.jpeg', '.tiff']:
            return OCRLoader().load(file_path)
        elif ext == '.csv':
            return CSVLoader().load(file_path)
        elif ext == '.docx':
            return DOCXLoader().load(file_path)
        elif ext == '.txt':
            return TXTLoader().load(file_path)
        else:
            logger.warning(f"Unsupported file extension: {ext}")
            return []
