import numpy as np
import soundfile as sf

def normalize_audio(x, peak=0.95):
    m = np.max(np.abs(x)) + 1e-9
    return (x / m) * peak

def pad_front(x, n):
    if n <= 0:
        return x
    return np.concatenate([np.zeros(n, dtype=x.dtype), x])

def mix_wavs(wav_paths, delays_ms, out_path, sr=22050):
    """
    wav_paths: list of wav file paths
    delays_ms: list of delays (same length), in milliseconds
    """
    waves = []
    max_len = 0

    for path, dms in zip(wav_paths, delays_ms):
        w, file_sr = sf.read(path, dtype="float32")
        if file_sr != sr:
            raise ValueError(f"Sample rate mismatch: {path} has {file_sr}, expected {sr}")

        delay_samples = int((dms / 1000.0) * sr)
        w = pad_front(w, delay_samples)

        waves.append(w)
        max_len = max(max_len, len(w))

    # pad all to same length
    padded = []
    for w in waves:
        if len(w) < max_len:
            w = np.pad(w, (0, max_len - len(w)), mode="constant")
        padded.append(w)

    mix = np.sum(np.stack(padded, axis=0), axis=0)

    # normalize to avoid clipping
    mix = normalize_audio(mix)

    sf.write(out_path, mix, sr)
    return out_path
