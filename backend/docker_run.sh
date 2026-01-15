docker run -it --rm --gpus all\
 -v "/mnt/e/Projects/speech agent":/app\
 -v /mnt/e/hf_cache:/root/.cache/huggingface\
 -v /mnt/e/tts_cache:/root/.local/share/tts\
 audio-ai