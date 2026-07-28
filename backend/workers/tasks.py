import os
import logging
from celery import Celery

logger = logging.getLogger(__name__)

# Initialize Celery
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("hospital_tasks", broker=redis_url, backend=redis_url)

@celery_app.task(bind=True, max_retries=3)
def process_ocr_task(self, file_path: str):
    logger.info(f"Celery processing OCR for {file_path}")
    try:
        from agents.multimodal.ocr import OCRProcessor
        result = OCRProcessor.process(file_path)
        return result
    except Exception as exc:
        logger.error(f"OCR task failed: {exc}")
        self.retry(exc=exc, countdown=5)

@celery_app.task(bind=True, max_retries=3)
def process_whisper_task(self, file_path: str):
    logger.info(f"Celery processing Audio for {file_path}")
    try:
        from agents.multimodal.speech import speech_processor
        result = speech_processor.process(file_path)
        return result
    except Exception as exc:
        logger.error(f"Whisper task failed: {exc}")
        self.retry(exc=exc, countdown=5)

@celery_app.task(bind=True)
def generate_embeddings_task(self, texts: list, collection: str):
    logger.info(f"Celery generating embeddings for {len(texts)} chunks in {collection}")
    try:
        from agents.rag.embeddings import EmbeddingEngine
        from agents.rag.vector_store import vector_store
        
        engine = EmbeddingEngine()
        embeddings = engine.generate_embeddings(texts)
        
        # Format docs for insertion
        docs = [{"content": t, "metadata": {"source": "background_job"}} for t in texts]
        vector_store.add_documents(collection, docs, embeddings)
        
        return {"status": "success", "count": len(texts)}
    except Exception as exc:
        logger.error(f"Embedding task failed: {exc}")
        return {"status": "error", "error": str(exc)}
