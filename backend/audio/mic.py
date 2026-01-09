import sounddevice as sd
import numpy as np

SAMPLE_RATE = 16000
DURATION = 4

def record_audio():
    print("🎤 Speak now...")
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate = SAMPLE_RATE,
        channels = 1,
        dtype = np.float32
    )
    sd.wait()
    print("⏹ Recording done")
    return audio.flatten()