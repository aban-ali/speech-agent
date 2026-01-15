from faster_whisper import WhisperModel

model = WhisperModel(
    "small",
    device = "cuda",
    compute_type = "int8"
)

def transcribe(path):
    segments, _ = model.transcribe(
        path,
        language="en",
        beam_size=1,
        vad_filter=True
    )

    text = " ".join(seg.text for seg in segments)
    return text.strip()
