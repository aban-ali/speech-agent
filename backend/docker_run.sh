docker run -it --rm --gpus all\
 -v hf_cache:/root/.cache/huggingface\
 -v tts_cache:/root/.local/share/tts\
 -v processed_audio:/app/sounds\
 -v audio_results:/app/ai-audio\
 -p 8000:8000 \
 speechagent-backend