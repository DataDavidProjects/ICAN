import os
import yaml
from dotenv import load_dotenv
from src.interaction.conversation import (
    Interaction,
)
from src.utils.agent_utils import (
    create_agents,
)

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
with open("config.yaml", "r") as f:
    context_config = yaml.safe_load(f)


user_request = context_config["user"]["request"]

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
    initial_prompt=user_request,
)

# Conduct the interaction rounds
brainstorm.conduct_interaction()

# Generate the final solution
final_output = brainstorm.final_solution()
print(final_output["final_output"])
