from TTS.api import TTS
import numpy as np
import soundfile as sf

class TTSEngine:
    def __init__(self, model_name="tts_models/en/vctk/vits"):
        self.tts = TTS(model_name=model_name, progress_bar=False, gpu=False)

    def speak(self, text, outpath, speaker=None):
        wav = self.tts.tts(text=text, speaker=speaker)
        wav = np.array(wav, dtype=np.float32)
        sf.write(outpath, wav, 22050)
        return outpath