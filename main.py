import os
import yaml
from dotenv import load_dotenv
from src.interaction.conversation import Interaction
from src.utils.agent_utils import create_agents, suggest_agents

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

with open("config.yaml", "r") as f:
    context_config = yaml.safe_load(f)


user_request = context_config["user"]["request"]
assistant_context = context_config["assistant"]["context"]

# Suggest agent details using the function
agent_details = suggest_agents(user_request, api_key, assistant_context)

print(agent_details)
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
