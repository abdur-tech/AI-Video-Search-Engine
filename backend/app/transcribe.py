import os
import torch
import whisperx
from .configs import settings
from typing import Any
import collections

# added below beacuse of torch security error for weight loading
_original_torch_load = torch.load

def _trusted_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)

torch.load = _trusted_load

device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "float32"

# Load models once at import time (worker will reuse)
audio_to_text_model = whisperx.load_model("distil-large-v3", device, compute_type=compute_type)

def transcribe_audio(audio_path: str):
    audio = whisperx.load_audio(audio_path)

    # Step 1: Transcribe with Distil-Whisper
    result = audio_to_text_model.transcribe(audio, batch_size=16, chunk_size=30)

    # Step 2: Align for accurate word-level timestamps
    align_model, metadata = whisperx.load_align_model(
        language_code=result["language"], device=device
    )
    result = whisperx.align(result["segments"], align_model, metadata, audio, device)

    # Cleanup temp audio
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return {
        "text": result["text"],
        "language": result["language"],
        "segments": [
            {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"],
                "words": seg.get("words", [])
            }
            for seg in result["segments"]
        ]
    }