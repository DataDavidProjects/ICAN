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
assistant_context = context_config["assistant"]["context"]

# Define agent details
agent_details = [
    {
        "agent_context": f"You are a accountant . {assistant_context}",
        "agent_name": "Davide",
    },
    {
        "agent_context": f"You are a economist. {assistant_context}",
        "agent_name": "Kyle",
    },
    {
        "agent_context": f"You are a investor. {assistant_context}",
        "agent_name": "Natalia",
    },
    {
        "agent_context": f"You are a marketing expert. {assistant_context} ",
        "agent_name": "Steven",
    },
]

# Create agents
agents = create_agents(api_key, agent_details)

# Initialize the Interaction class
brainstorm = Interaction(
    agents=agents,
    rounds=2,
    initial_prompt=user_request,
)

# Conduct the interaction rounds
brainstorm.conduct_interaction()

# Generate the final solution
final_output = brainstorm.final_solution()
print(final_output["final_output"])
