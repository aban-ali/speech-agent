from llama_cpp import Llama

llm = Llama(
    model_path="/root/.cache/huggingface/gemma-3-1b-it-Q4_0.gguf",
    n_ctx = 512,
    n_gpu_layers = -1,
    n_threads = 8,
    n_batch = 256,
    verbose = False
)