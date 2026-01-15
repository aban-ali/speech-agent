from llm.agent import Agent, GroqAgent
from llm.model import llm
from llm.prompts import AGENTS

# Initial function for generating response
def run_agents(user_text):
    agents = [
        Agent(agent["name"], agent["prompt"], agent["temperature"], llm) 
        for agent in AGENTS
    ]
    return [agent.generate(user_text) for agent in agents]

# modified version to support multi-threading....
def run_agent_stream(user_text, mode="local"):
    if mode == "local":
        agents = [
            Agent(agent["name"], agent["prompt"], agent["temperature"], llm) 
            for agent in AGENTS
        ]
    else:
        agents = [
            GroqAgent(agent["name"], agent["prompt"], agent["temperature"])
            for agent in AGENTS
        ]

    for agent in agents:
        yield agent.generate(user_text)