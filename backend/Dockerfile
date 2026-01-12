FROM pytorch/pytorch:2.9.1-cuda12.6-cudnn9-runtime

WORKDIR /app
COPY requirements.txt .

# 🔒 Force CPU-only llama-cpp
ENV FORCE_CMAKE=1
ENV CMAKE_ARGS="-DLLAMA_CUBLAS=off"
ENV CMAKE_BUILD_PARALLEL_LEVEL=2

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        cmake \
        python3-dev \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

# 🔑 prefer binary if available, fallback to build
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

CMD ["bash"]