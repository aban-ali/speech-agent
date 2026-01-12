from llm.agent import Agent
from llm.model import llm
from llm.prompts import AGENTS
# from concurrent.futures import ThreadPoolExecutor

def run_agents(user_text):
    agents = [
        Agent(agent["name"], agent["prompt"], agent["temperature"], llm) 
        for agent in AGENTS
    ]
    # with ThreadPoolExecutor(max_workers=len(agents)) as executor:
    #     futures = [
    #         executor.submit(agent.generate, user_text)
    #         for agent in agents
    #     ]
    # print("Executed THread pool")
    # print(futures)
    # return [f.result() for f in futures]

    return [agent.generate(user_text) for agent in agents]