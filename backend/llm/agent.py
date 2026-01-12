class Agent:
    def __init__(self, name, prompt, temperature, llm):
        self.name = name
        self.prompt = prompt
        self.temperature = temperature
        self.llm = llm

    def generate(self, user_text):
        prompt = f"""
SYSTEM:
{self.prompt}
Your response should be strictly between 30 to 50 words.
Embrace the personality and give only one response without any explanation or alternative and do not repeat yourself.

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
            "text" : output["choices"][0]["text"].strip()
        }