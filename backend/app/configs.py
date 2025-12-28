from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CELERY_BROKER_URL: str = 'redis://localhost:6379/0'
    VIDEO_UPLOAD_DIR: str = "videos"
    AUDIO_TEMP_DIR: str = "audio"
    CELERY_RESULT_BACKEND: str = 'redis://localhost:6379/1'
settings = Settings()