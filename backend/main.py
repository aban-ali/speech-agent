from time import perf_counter

from stt.whisper import transcribe
from llm.orchestrator import run_agents
from tts.engine import TTSEngine

tts = TTSEngine()

audio_path = "./sounds/Recording (2).m4a"
text = transcribe(audio_path)

print("\n🧠 YOU SAID:", text)

b = perf_counter()
responses = run_agents(text)

# simple mapping
speaker_map = {
    "chaos": "p239",
    "analyst": "p230",
    "hype": "p363",
    "realist": "p243",
}

print("\n--- AGENTS ---")
for r in responses:
    outpath = f"./ai-audio/{r['agent'].upper()}.wav"
    print(f"\n[{r['agent'].upper()}]")
    print(r["text"].strip())
    print( tts.speak(r["text"], outpath, speaker_map.get(r["agent"])) )

print(f"Total time taken by all the agents- {perf_counter() - b:.2f}")