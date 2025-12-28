import os
import torch
import whisperx
from .configs import settings
from typing import Any
import collections
import numpy as np

# added below beacuse of torch security error for weight loading
_original_torch_load = torch.load

def _trusted_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)

torch.load = _trusted_load

device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "float32"

# Load models once at import time (worker will reuse)
audio_to_text_model = whisperx.load_model("small.en", device, compute_type=compute_type)


def format_transcription_result(result: dict) -> dict:
    def to_native(value):
        return value.item() if isinstance(value, np.generic) else value

    text = result.get("text", "").strip()
    language = result.get("language", "unknown")

    segments = []
    for seg in result.get("segments", []):
        if not isinstance(seg, dict):
            continue
        words = seg.get("words", [])
        # Convert word timestamps/scores if present
        cleaned_words = [
            {
                "word": w.get("word", ""),
                "start": to_native(w.get("start")),
                "end": to_native(w.get("end")),
                "score": to_native(w.get("score", 0.0))
            }
            for w in words
            if isinstance(w, dict)
        ]

        segments.append({
            "start": to_native(seg.get("start")),
            "end": to_native(seg.get("end")),
            "text": seg.get("text", ""),
            "words": cleaned_words
        })

    return {
        "text": text,
        "language": language,
        "segments": segments
    }
def transcribe_audio(audio_path: str):
    audio = whisperx.load_audio(audio_path)
    # Step 1: Transcribe with Distil-Whisper
    result = audio_to_text_model.transcribe(audio, batch_size=16, chunk_size=30)

    # Step 2: Align for accurate word-level timestamps
    align_model, metadata = whisperx.load_align_model(
        language_code=result["language"], device=device
    )
    result = whisperx.align(result["segments"], align_model, metadata, audio, device)
    formatted_result=format_transcription_result(result)
    # Cleanup temp audio
    if os.path.exists(audio_path):
        os.remove(audio_path)
    return formatted_result