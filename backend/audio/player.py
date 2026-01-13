"""
This file is not put in action since I was working in Docker 
and I did not give my speaker control to the container. 

The structure for playing the audio will be similar to this....
"""
import sounddevice as sd

SAMPLE_RATE = 22050

def play_audio(wav):
    sd.play(wav, SAMPLE_RATE)
    sd.wait()