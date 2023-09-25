from typing import List, Dict, Union
from src.agents.agent import (
    Agent,
)


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

    def __str__(self) -> str:
        """
        Provide a string representation of the Interaction instance.

        Returns:
            str: A string representation.
        """
        agent_names = ", ".join(list(self.agents.keys()))
        return f"Interaction(Agents: [{agent_names}], Rounds: {self.rounds}, Initial Prompt: {self.initial_prompt})"

    def __repr__(self):
        return f"User(username='{self.username}', password='{self.password}')"

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
        """
        Generate the final solution based on the contributions from all agents.

        Returns:
            Dict[str, Union[str, List[Dict[str, str]]]]: A dictionary containing the final solution as a string,
            and the dialog history as a list of dictionaries.
        """
        most_recent_contributions = {}

        for entry in reversed(self.internal_history):
            if entry["role"] == "assistant":
                most_recent_contributions[entry["agent_name"]] = entry["content"]
        print("*" * 100)
        final_output = "Final Solution: Based on the latest insights, "
        final_output += " ".join(
            [
                f"{agent_name} suggests: {suggestion};"
                for agent_name, suggestion in most_recent_contributions.items()
            ]
        )

        return {"final_output": final_output, "shared_history": self.shared_history}
