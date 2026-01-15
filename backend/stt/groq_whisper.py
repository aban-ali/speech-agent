from groq import Groq
from dotenv import DotEnv

env = DotEnv()

client = Groq(
      api_key = env.get("GROQ_API_KEY")
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