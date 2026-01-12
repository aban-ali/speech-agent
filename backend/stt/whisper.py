from faster_whisper import WhisperModel
from time import time

model = WhisperModel(
    "small",
    device = "cuda",
    compute_type = "int8"
)

def transcribe(path):
    start = time()
    segments, _ = model.transcribe(
        path,
        language="en",
        beam_size=1,
        vad_filter=True
    )

    text = " ".join(seg.text for seg in segments)
    print(f"⏱ Took {time() - start:.2f}s")
    return text.strip()
