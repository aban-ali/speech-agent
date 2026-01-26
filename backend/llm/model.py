from llama_cpp import Llama
import os
from huggingface_hub import hf_hub_download

if not os.path.exists("/root/.cache/huggingface/gemma-3-1b-it-Q8_0.gguf"):
    print("Downloading model...")
    path = hf_hub_download(
        repo_id="ggml-org/gemma-3-1b-it-GGUF",
        filename="gemma-3-1b-it-Q8_0.gguf",
        local_dir="/root/.cache/huggingface/",
        local_dir_use_symlinks=False
    )
    print(f"Model downloaded to {path}")

llm = Llama(
    model_path="/root/.cache/huggingface/gemma-3-1b-it-Q8_0.gguf",
    n_ctx = 512,
    n_gpu_layers = -1,
    n_threads = 8,
    n_batch = 256,
    verbose = False
)