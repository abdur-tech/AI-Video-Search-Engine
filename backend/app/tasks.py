from celery import Celery

from .utils import extract_audio
from .configs import settings
celery = Celery(
    __name__, 
    broker=settings.CELERY_BROKER_URL,       
    backend=settings.CELERY_RESULT_BACKEND,  
)
celery.conf.update(
    task_always_eager=False,       
    task_eager_propagates=False,
    worker_prefetch_multiplier=1,  # Good for long-running tasks (like transcription)
    task_acks_late=True,
    result_expires=3600,
)
@celery.task(name="process_video")
def process_video(video_path: str, audio_path: str):
    try:
        # Extract audio
        extract_audio(video_path, audio_path)
        # Transcribe
        from .transcribe import transcribe_audio
        result = transcribe_audio(audio_path)
        with open("tmp_output.txt", 'w', encoding='utf-8') as file:
            file.write(str(result))
        return {"status": "success", "transcript": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}