import numpy as np
import soundfile as sf

class TimelineMixer:
    def __init__(self, sr=22050):
        self.sr = sr
        self.buffer = np.zeros(1, dtype=np.float32)

    def _ensure_len(self, n):
        if len(self.buffer) < n:
            self.buffer = np.pad(self.buffer, (0, n - len(self.buffer)), mode="constant")

    def add_wav(self, wav, start_ms=0, gain=0.7):
        if isinstance(wav, str):
            wav, file_sr = sf.read(wav, dtype="float32")
            if file_sr != self.sr:
                raise ValueError(f"SR mismatch: {wav} has {file_sr}, expected {self.sr}")

        start = int((start_ms / 1000.0) * self.sr)
        end = start + len(wav)
        self._ensure_len(end)
        self.buffer[start:end] += wav * gain

    def normalize(self, peak=0.95):
        m = np.max(np.abs(self.buffer)) + 1e-9
        self.buffer = (self.buffer / m) * peak

    def write(self, out_path):
        self.normalize()
        sf.write(out_path, self.buffer, self.sr)
        return out_path
