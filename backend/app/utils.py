import os
import ffmpeg
from fastapi import UploadFile

def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "wb") as out_file:
        content = upload_file.file.read()
        out_file.write(content)
    return destination

def extract_audio(video_path: str, audio_path: str) -> str:
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, acodec="pcm_s16le", ar=16000, vn=True)
            .overwrite_output()
            .run(quiet=True)
        )
        return audio_path
    except ffmpeg.Error as e:
        print("abc")
        raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}")