from time import perf_counter

from stt.whisper import transcribe
from llm.orchestrator import run_agents

audio_path = "./audio/Recording (2).m4a"
text = transcribe(audio_path)

print("\n🧠 YOU SAID:", text)

responses = run_agents(text)

b = perf_counter()
print("\n--- AGENTS ---")
for r in responses:
    print(f"\n[{r['agent'].upper()}]")
    print(r["text"].strip())

print(f"Total time taken by all the agents- {perf_counter() - b:.2f}")