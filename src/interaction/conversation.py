from typing import List, Dict, Union
import os
from dotenv import load_dotenv
from src.agents.agent import (
    Agent,
)

# Load environment variables
load_dotenv()


class Interaction:
    def __init__(
        self, agents: Dict[str, Agent], rounds: int, initial_prompt: str
    ) -> None:
        """
        Initialize the Interaction class with multiple agents, number of rounds, and the initial problem prompt.

        Parameters:
            agents (Dict[str, Agent]): Dictionary of Agent objects participating in the Interaction.
            rounds (int): Number of rounds for the Interaction session.
            initial_prompt (str): The initial problem prompt to start the Interaction.
        """
        self.agents = agents
        self.rounds = rounds
        self.initial_prompt = initial_prompt
        self.internal_history: List[Dict[str, str]] = []
        self.shared_history: List[Dict[str, str]] = [
            {"role": "user", "content": self.initial_prompt}
        ]

        # Initialize the special AnalyzerAgent
        analysis_context = """
        You are an expert in analyzing and summarizing discussions. Your task is to 
        provide a concise summary and solution based on the shared history of interactions.

        Return:
        1. A Summary paragraph of the problem and summarized contributions.
        2. Solution paragraph with the final solution with all necessary details in depth. 
        Respect the requested formats if specified
        """
        self.analyzer_agent = Agent(
            api_key=os.environ.get("OPENAI_API_KEY"),
            agent_context=analysis_context,
            agent_name="AnalyzerAgent",
        )

    def __str__(self) -> str:
        """
        Provide a string representation of the Interaction instance.

        Returns:
            str: A string representation.
        """
        agent_names = ", ".join(list(self.agents.keys()))
        return f"Interaction(Agents: [{agent_names}], Rounds: {self.rounds}, Initial Prompt: {self.initial_prompt})"

    def __repr__(self):
        return f"Interaction(request='{self.initial_prompt}', agents='{self.agents}', rounds='{self.rounds}')"

    def conduct_round(self) -> None:
        """
        Conduct a single round of Interaction where each agent contributes to the shared history.

        Returns:
            None
        """
        for agent_name, agent in self.agents.items():
            agent.listen(self.shared_history)
            response, _ = agent.reply()
            print("-" * 100)
            print(f"{agent_name}: \n {response}")
            self.shared_history.append({"role": "assistant", "content": response})
            self.internal_history.append(
                {"role": "assistant", "agent_name": agent_name, "content": response}
            )

    def conduct_interaction(self) -> None:
        """
        Conduct multiple rounds of Interaction based on the specified number of rounds.

        Returns:
            None
        """
        for _ in range(self.rounds):
            self.conduct_round()

    def final_solution(self) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        # Use the AnalyzerAgent to get a concise summary
        entire_history = "\n".join([entry["content"] for entry in self.shared_history])
        analysis, _ = self.analyzer_agent.chat_completion(entire_history)
        print("*" * 100)
        final_output = "Final Solution: Based on the analysis, \n" + analysis

        return {"final_output": final_output, "shared_history": self.shared_history}
