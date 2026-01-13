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
Your response should be strictly between 30 to 50 words.
Write response that should sound like real human speaking out loud.
Use emotion through word choice, rhythm, and punctuation, like using words such as - aaah, arrrggh, helloooo!!!, damn!!, hmmm.
Embrace the personality and give only one meaningful response without any explanation or alternative.

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