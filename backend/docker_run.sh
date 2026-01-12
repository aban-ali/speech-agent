docker run -it --rm --gpus all\
 -v "/mnt/e/Projects/speech agent":/app\
 -v /mnt/e/hf_cache:/root/.cache/huggingface\
 ai-audio