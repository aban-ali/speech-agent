# 🎭 Voices in Your Head

A real-time multi-agent voice AI system where a single spoken input triggers
multiple AI personalities that respond, interrupt, and overlap in audio.

Built to explore **speech-first AI UX**, **multi-agent orchestration**, and
**low-latency voice pipelines** using both **local open-source models** and
**proprietary APIs**.

---

## ✨ Features

- 🎙️ **Speech-to-Text** (local Whisper / Groq Whisper)
- 🧠 **Multi-agent LLM system**
  - Different personalities
  - Independent reasoning
  - Sequential-safe inference (llama.cpp)
- 🔊 **Text-to-Speech**
  - Local TTS (Coqui VITS)
  - Proprietary TTS (Groq / Orpheus)
- 🎧 **Overlapping audio mixing**
  - Agents interrupt naturally
  - Human-like timing offsets
- ⚡ **Streaming-style UX**
  - Audio starts as soon as agents finish
- 🌐 **React frontend**
  - Browser-based audio recording
  - Live transcript & agent cards
- 🐳 **Fully Dockerized**
- 🔁 **Hybrid mode**
  - Switch between local models and Grok APIs

---

## 🧠 Architecture (High-Level)

```
Browser(Mic)
↓
FastAPI Backend
↓
STT → Agent Orchestrator → TTS
↓
Timeline Audio Mixer
↓
Frontend Audio Playback
```

---

## 🛠️ Tech Stack

**Backend**
- Python, FastAPI
- faster-whisper / Groq Whisper
- llama-cpp (GGUF models)
- Coqui TTS (VITS)
- Groq API (LLM + TTS)
- NumPy, ffmpeg

**Frontend**
- React (Vite)
- Web Audio API
- MediaRecorder API

**Infra**
- Docker + NVIDIA CUDA
- Hugging Face Hub (auto model download)

---

## 🚀 Modes

### Local Mode
- STT: Whisper (local)
- LLM: llama.cpp (GGUF)
- TTS: Coqui VITS
- Fully offline (after model download)

### Grok Mode
- STT: Whisper Large (Groq)
- LLM: Proprietary (Groq)
- TTS: Orpheus
- Low-latency cloud inference

---

## ▶️ Running the Project

```bash
docker compose up
```
---

## 🎯 Why This Project

Most voice assistants are single-response systems.
This project explores:
- Voice as a primary interface
- Multiple AI perspectives in real time
- How timing and overlap change perceived intelligence

## 📌 Future Work

True streaming TTS (chunk-level)
Emotion control per agent
Mobile-friendly UI
Agent-to-agent debates

---

## 📄 License

MIT

