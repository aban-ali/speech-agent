from groq import Groq
from dotenv import DotEnv

env = DotEnv()

class GroqAgent:
    def __init__(self, name, prompt, temperature, model="openai/gpt-oss-20b"):
        self.client = Groq(
            api_key=env.get("GROQ_API_KEY")
        )
        self.name = name
        self.prompt = prompt
        self.temperature = temperature
        self.model = model

    def groq_generate(self, user_text):
        response = self.client.chat.completions.create(
            messages = [
                {
                    "role": "system",
                    "content": f"'{self.prompt}'\
                        Embrace the personality and give response strictly between 30 to 50 words.\
                        Write response that should sound like real human speaking out loud and direct.\
                        Use emotion through word choice, rhythm, and punctuation."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            model = self.model,
            temperature = self.temperature,
            max_completion_tokens = 128,
            top_p=0.9
        )
        return {
            "agent": self.name,
            "text": response.choices[0].message.content
        }


class Agent:
    def __init__(self, name, prompt, temperature, llm):
        self.name = name
        self.prompt = prompt
        self.temperature = temperature
        self.llm = llm

    def clean_text(self, text):
        return text.split("*")[0]

    def generate(self, user_text):
        prompt = f"""
SYSTEM:
{self.prompt}
Embrace the personality and give only one meaningful response without any explanation or alternative.
Your response should be strictly between 30 to 50 words.
Write response that should sound like real human speaking out loud.
Use emotion through word choice, rhythm, and punctuation.

USER:
{user_text}

ASSISTANT:
"""
        output = self.llm(
            prompt,
            temperature = self.temperature,
            max_tokens = 60,
            stop = ["USER:", "SYSTEM:"]
        )
        return {
            "agent" : self.name,
            "text" : self.clean_text( output["choices"][0]["text"].strip() )
        }