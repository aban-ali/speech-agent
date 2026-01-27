FROM pytorch/pytorch:2.9.1-cuda12.6-cudnn9-devel

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# System deps
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        cmake \
        python3-dev \
        ffmpeg \
        espeak-ng \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

# 1) Install llama-cpp-python
ENV FORCE_CMAKE=1
ENV CMAKE_ARGS="-DLLAMA_CUBLAS=off"
ENV CMAKE_BUILD_PARALLEL_LEVEL=2
RUN pip install --no-cache-dir llama-cpp-python

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY audio /app/audio
COPY llm /app/llm
COPY stt /app/stt
COPY tts /app/tts
COPY main.py /app/
COPY .env /app/

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]