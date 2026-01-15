from time import perf_counter
import random
import argparse

from stt.whisper import transcribe
from stt.groq_whisper import groq_transcribe

from llm.orchestrator import run_agents, run_groq_agents
from tts.engine import TTSEngine, GroqEngine

from audio.mixer import mix_wavs

tts = TTSEngine()
groq_tts = GroqEngine()

def local_workflow():
    print("📍 Local Inferencing Starting....")

    audio_path = "./sounds/Recording (2).m4a"
    text = transcribe(audio_path)
    responses = run_agents(text)

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
        tts.speak(r["text"], outpath, speaker_map.get(r["agent"]))

    wav_paths = [
        "./ai-audio/CHAOS.wav",
        "./ai-audio/ANALYST.wav",
        "./ai-audio/HYPE.wav",
        "./ai-audio/REALIST.wav",
    ]
    delays_ms = [0, random.randint(80,160), random.randint(180,320), random.randint(120,260)]
    mix_wavs(
        wav_paths=wav_paths,
        delays_ms=delays_ms,
        out_path="./ai-audio/final_mix.wav",
        sr=22050
    )
    print("✅ Local Inferencing completed")



def groq_workflow():
    print("📍 Inferencing using Groq API is Starting....")

    audio_path = "./sounds/Recording.m4a"
    text = groq_transcribe(audio_path)
    responses = run_groq_agents(text)

    speaker_map = {
        "chaos": "troy",
        "analyst": "autumn",
        "hype": "austin",
        "realist": "hannah",
    }

    print("\n--- AGENTS ---")
    for r in responses:
        outpath = f"./ai-audio/{r['agent'].upper()}.wav"
        print(f"\n[{r['agent'].upper()}]")
        print(r["text"].strip())
        groq_tts.speak(r["text"], outpath, speaker_map.get(r["agent"]))

    wav_paths = [
        "./ai-audio/CHAOS.wav",
        "./ai-audio/ANALYST.wav",
        "./ai-audio/HYPE.wav",
        "./ai-audio/REALIST.wav",
    ]
    delays_ms = [0, random.randint(80,160), random.randint(180,320), random.randint(120,260)]
    mix_wavs(
        wav_paths=wav_paths,
        delays_ms=delays_ms,
        out_path="./ai-audio/final_groq_mix.wav",
        sr=24000
    )
    print("✅ Inferencing with Groq API completed")


def parse_args():
    parser = argparse.ArgumentParser("Speech Agent CLI")
    parser.add_argument(
        "--local", 
        action="store_true", 
        help="run inference with local AI models\
            STT model: faster_whisper('small')\
            LLM: gemma-3-1b-it-Q4_0.gguf\
            TTS model: tts_models/en/vctk/vits"
        )
    parser.add_argument(
        "--groq",
        action="store_true",
        help="run inference with propreitary models present on Groq.\
            STT model: whisper-large-v3-turbo\
            LLM: openai/gpt-oss-20b\
            TTS model: canopylabs/orpheus-v1-english"
    )
    parser.add_argument(
        "--server",
        action="store_true",
        help="Run the API server."
    )

    args = parser.parse_args()
    return [args.local, args.groq, args.server]

if __name__=="__main__":
    local, groq, server = parse_args()
    if(local):
        local_workflow()
    elif(groq):
        groq_workflow()
    elif(server):
        pass
    else:
        print("Invalid operation. Please continue with '-h' flag to get all option details.")