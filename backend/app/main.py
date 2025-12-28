from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException
from uuid import uuid4
import os
from .tasks import process_video
from .utils import save_upload_file
from .configs import settings

app = FastAPI(title="AI Video Transcription API")

@app.post("/upload-video/")
async def upload_video(file: UploadFile):
    if not file.filename.lower().endswith(".mp4"):
        raise HTTPException(400, detail="Only .mp4 files allowed")

    video_id = str(uuid4())
    video_path = os.path.join(settings.VIDEO_UPLOAD_DIR, f"{video_id}.mp4")
    audio_path = os.path.join(settings.AUDIO_TEMP_DIR, f"{video_id}.wav")

    # Save video file
    save_upload_file(file, video_path)

    # Fire async Celery task
    process_video.delay(video_path, audio_path)
    return {
        "video_id": video_id,
        "status": "uploaded and processing started",
        "message": "Transcription running in background (Celery)"
    }

@app.get("/")
def root():
    return {"message": "Video Transcription API with Distil-Whisper + Celery"}