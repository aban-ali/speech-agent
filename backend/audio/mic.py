"""
This file is not put in action since I was working in Docker 
and I did not give my mic control to the container. 

The structure for recording the audio will be similar to this....
"""

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