from typing import List, Dict, Tuple, Optional
from src.agents.agent import Agent


def create_agents(
    api_key: str, agent_details: List[Dict[str, str]]
) -> Dict[str, "Agent"]:
    """
    Create multiple agents based on provided details and a common API key.

    Parameters:
        api_key (str): The OpenAI API key to be used for all agents.
        agent_details (List[Dict[str, str]]): List of dictionaries containing details for each agent.
            Each dictionary must have 'expertise' and 'agent_name' keys.

    Returns:
        Dict[str, Agent]: Dictionary of agents, keyed by their names.
    """
    return {
        detail["agent_name"]: Agent(
            api_key=api_key,
            agent_context=detail["agent_context"],
            agent_name=detail["agent_name"],
        )
        for detail in agent_details
    }
