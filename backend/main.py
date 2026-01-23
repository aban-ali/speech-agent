from os.path import basename
from time import strftime
import random
import uvicorn
import argparse
import shutil
import subprocess
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from stt.whisper import transcribe
from stt.groq_whisper import groq_transcribe

from llm.orchestrator import run_agent_stream
from tts.engine import TTSEngine, GroqEngine

# from audio.mixer import mix_wavs
from audio.timeline_mixer import TimelineMixer

warnings.filterwarnings("ignore")
tts = TTSEngine()
groq_tts = GroqEngine()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/files", StaticFiles(directory="./ai-audio"), name="files")


base_offsets = {
    "chaos": 0,
    "analyst": 120,
    "hype": 200,
    "realist": 160,
    "sarcastic": 180
}

def local_workflow(audio_path):
    print("📍 Local Inferencing Starting....")

    text = transcribe(audio_path)
    speaker_map = {
        "chaos": "p239",
        "analyst": "p230",
        "hype": "p363",
        "realist": "p243",
        "sarcastic": "p351"
    }
    tasks = []
    mixer = TimelineMixer()
    agent_data = []
    with ThreadPoolExecutor(max_workers=5) as ex:
        for r in run_agent_stream(text):
            print(f"\n[{r['agent'].upper()}] {r['text'].strip()}")
            agent_data.append({"agent": r["agent"].upper(), "text": r["text"]})
            tasks.append(
                ex.submit(
                    tts.speak, r["text"], r["agent"], speaker_map.get(r["agent"])
                )
            )

        for task in as_completed(tasks):
            wav, agent = task.result()
            offset = random.randint(0, 120)
            start_ms = base_offsets.get(agent, 0) + offset
            mixer.add_wav(wav, start_ms=start_ms, gain=0.75)
            mixer.write("./ai-audio/final_mix.wav")

    print("✅ Local Inferencing completed")
    return {
        "transcript": text,
        "agents": agent_data,
        "output_audio": "/files/final_mix.wav"
    }


def groq_workflow(audio_path):
    print("📍 Inferencing using Groq API is Starting....")

    text = groq_transcribe(audio_path)

    speaker_map = {
        "chaos": "troy",
        "analyst": "autumn",
        "hype": "austin",
        "realist": "hannah",
        "sarcastic": "austin"
    }
    tasks = []
    mixer = TimelineMixer(24000)
    agent_data = []
    with ThreadPoolExecutor(max_workers=5) as ex:
        for r in run_agent_stream(text, "grok"):
            outpath = f"./ai-audio/{r['agent'].upper()}.wav"
            print(f"[{r['agent'].upper()}] {r['text'].strip()}")
            agent_data.append({"agent": r["agent"].upper(), "text": r["text"]})
            tasks.append(
                ex.submit(
                    groq_tts.speak, r["text"], outpath, speaker_map.get(r["agent"])
                )
            )
        for task in as_completed(tasks):
            path = task.result()
            agent = basename(path).split(".")[0].lower()
            offset = random.randint(0, 120)
            start_ms = base_offsets.get(agent, 0) + offset
            mixer.add_wav(path, start_ms, gain=0.75)
            mixer.write("/files/final_groq_mix.wav")

    print("✅ Inferencing with Groq API completed")
    return {
        "transcript": text,
        "agents": agent_data,
        "output_audio": "./ai-audio/final_groq_mix.wav"
    }


@app.post("/run")
async def upload_audio(file: UploadFile = File(...), mode: str = "local"):
    time = strftime("%d-%a %H:%M:%S")
    file_location = f"./sounds/{time}_{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    outpath = f"./sounds/{time}_processed.wav"
    subprocess.run(["ffmpeg", "-y", "-i", file_location, "-ar", "24000", outpath])
    res = groq_workflow(outpath) if mode=="grok" else local_workflow(outpath)
    return res

@app.get("/health/")
async def health_check():
    return {"status": "ok"}

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

    args = parser.parse_args()
    return [args.local, args.groq]

if __name__=="__main__":
    local, groq = parse_args()
    if(local):
        local_workflow()
    elif(groq):
        groq_workflow()
    else:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)