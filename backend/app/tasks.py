from celery import Celery
from .transcribe import transcribe_audio
from .utils import extract_audio
from .configs import settings
import os

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_BROKER_URL
celery.conf.result_backend=settings.CELERY_RESULT_BACKEND
# Required for memory backend to work without a separate Redis server
celery.conf.task_always_eager = True  
celery.conf.task_eager_propagates = True

@celery.task(name="process_video")
def process_video(video_path: str, audio_path: str):
    try:
        # Extract audio
        extract_audio(video_path, audio_path)

        # Transcribe
        result = transcribe_audio(audio_path)

        # Here you could save result to DB, vector index, etc.
        print("Transcription completed:", result["text"][:200])

        return {"status": "success", "transcript": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}