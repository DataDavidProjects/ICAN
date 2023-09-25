import os
from dotenv import load_dotenv
from src.agents.agent import Agent
from src.interaction.conversation import (
    Interaction,
)
from src.utils.agent_utils import (
    create_agents,
)

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

# Define agent details
agent_details = [
    {"expertise": "Fullstack Development", "agent_name": "Davide"},
    {"expertise": "Marketing", "agent_name": "Natalia"},
    {"expertise": "Data Science", "agent_name": "Steven"},
]

# Create agents
agents = create_agents(api_key, agent_details)

# Initialize the Interaction class
brainstorm = Interaction(
    agents=agents,
    rounds=3,
    initial_prompt="I want to build a simple webapp that prints 'Hello World' to a user. How can I do it?",
)

# Conduct the Interaction rounds
brainstorm.conduct_interaction()

# Generate the final solution
final_output = brainstorm.final_solution()
print(final_output["final_output"])
