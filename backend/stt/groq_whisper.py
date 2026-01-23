from groq import Groq
from os import getenv

client = Groq(
      api_key = getenv("GROQ_API_KEY")
)

def groq_transcribe(filename, model="whisper-large-v3-turbo"):
        with open(filename, "rb") as file:
            transcription = client.audio.transcriptions.create(
            file=file, 
            model=model,
            prompt="Specify context or spelling",
            language="en",
            temperature=0.0
            )
        return transcription.text.strip()