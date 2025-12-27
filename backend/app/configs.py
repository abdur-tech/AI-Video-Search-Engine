from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CELERY_BROKER_URL: str = 'memory://'
    VIDEO_UPLOAD_DIR: str = "videos"
    AUDIO_TEMP_DIR: str = "audio"
    CELERY_RESULT_BACKEND: str = 'cache+memory://'
settings = Settings()