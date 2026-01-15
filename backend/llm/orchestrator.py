from llm.agent import Agent, GroqAgent
from llm.model import llm
from llm.prompts import AGENTS
from concurrent.futures import ThreadPoolExecutor

def run_agents(user_text):
    agents = [
        Agent(agent["name"], agent["prompt"], agent["temperature"], llm) 
        for agent in AGENTS
    ]
    return [agent.generate(user_text) for agent in agents]

def run_groq_agents(user_text):
    agents = [
        GroqAgent(agent["name"], agent["prompt"], agent["temperature"])
        for agent in AGENTS
    ]
    with ThreadPoolExecutor(max_workers=len(agents)) as executor:
        futures = [
            executor.submit(agent.groq_generate, user_text)
            for agent in agents
        ]
    return [f.result() for f in futures]