from TTS.api import TTS
from groq import Groq
from dotenv import DotEnv
import numpy as np
import soundfile as sf
import os

env = DotEnv()

class TTSEngine:
    def __init__(self, model_name="tts_models/en/vctk/vits"):
        self.tts = TTS(model_name=model_name, progress_bar=False, gpu=False)

    def speak(self, text, agent, speaker=None):
        wav = self.tts.tts(text=text, speaker=speaker)
        wav = np.array(wav, dtype=np.float32)
        # for testing purpose...
        sf.write(f"./ai-audio/{agent}.wav", wav, 22050)

        return (wav, agent)
    

class GroqEngine:
    def __init__(self):
        self.client = Groq(
            api_key = env.get("GROQ_API_KEY")
        )
    
    def speak(self, text, outpath, speaker, model="canopylabs/orpheus-v1-english"):
        wav = self.client.audio.speech.create(
            model = model,
            input = text,
            voice = speaker,
            response_format = "wav"
        )
        wav.write_to_file(outpath)
        return outpath
