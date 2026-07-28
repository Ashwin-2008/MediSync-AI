import logging
from typing import Dict, Any

try:
    import pydicom
except ImportError:
    pydicom = None

logger = logging.getLogger(__name__)

class DICOMProcessor:
    """Extracts metadata from DICOM medical images."""
    
    @staticmethod
    def process(file_path: str) -> Dict[str, Any]:
        if not pydicom:
            logger.warning("pydicom not installed.")
            return {"metadata": {"PatientName": "Mock Patient", "Modality": "X-RAY"}}
            
        try:
            ds = pydicom.dcmread(file_path)
            # Extract safe text metadata (excluding pixel data which is huge)
            metadata = {}
            for elem in ds:
                if elem.tag != pydicom.tag.Tag(0x7fe0, 0x0010): # Exclude PixelData
                    metadata[elem.keyword] = str(elem.value)
                    
            return {
                "metadata": metadata,
                "modality": ds.get("Modality", "Unknown"),
                "patient_id": ds.get("PatientID", "Unknown")
            }
        except Exception as e:
            logger.error(f"DICOM processing failed: {e}")
            return {"error": str(e)}
