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
    try:
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        ffmpeg.input(video_path).output(
                audio_path,
                f='mp4',
                acodec="pcm_s16le",  # 16-bit PCM
                ar=16000,            # 16kHz sample rate
                ac=1,                # Mono
                vn=True              # No video
            ).overwrite_output().run(capture_stdout=True, capture_stderr=True)
        return audio_path
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        raise e
    
