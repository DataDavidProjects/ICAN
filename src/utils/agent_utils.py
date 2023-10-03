from typing import List, Dict, Tuple, Optional
from src.agents.agent import Agent
import random
import openai
import re


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


def suggest_agents(
    prompt: str, api_key: str, assistant_context: str, team_size: int = 3
) -> list:
    """
    Use OpenAI to analyze a given prompt and suggest relevant agent details.

    Parameters:
        prompt (str): The problem or task description.
        api_key (str): OpenAI API key.
        assistant_context (str): A context description to be added to each agent's context.

    Returns:
        list: A list of dictionaries containing agent details.
    """

    competency_suggester_context = f"""
    You are an expert HR suggesting which job title or expertise a potential CEO
    required to consult. Given a task or problem, list out the competencies that would be best suited 
    to solve it. Please list only the most {team_size} important competencies/job titles in bullet points.
    
    Expected Output:
    * Design: the ability to create pleasing and functional UX and UI.
    * Development: proficiency in coding and software creation.
    * Digital Marketing: understanding of online promotional strategies.
    * Management: leadership and organizational skills.
    """

    openai.api_key = api_key
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": competency_suggester_context},
            {"role": "user", "content": prompt},
        ],
    }

    response = openai.ChatCompletion.create(**payload)

    # Extract competencies from the response using regex
    competencies = re.findall(
        r"\*\s*(.*?)(?:\n|$)", response.choices[0].message.content
    )

    agent_details = [
        {
            "agent_context": f"Your skills are \n {competency}. {assistant_context}",
            "agent_name": f"Agent_{name}",
        }
        for name, competency in enumerate(competencies)
    ]

    return agent_details
