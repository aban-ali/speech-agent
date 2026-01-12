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
your response should be in less than 50 words. Embrace the personality and give response without any explanation.

USER:
{user_text}

ASSISTANT:
"""
        output = self.llm(
            prompt,
            temperature = self.temperature,
            max_tokens = 100,
            stop = ["USER:"]
        )
        return {
            "agent" : self.name,
            "text" : output["choices"][0]["text"].strip()
        }