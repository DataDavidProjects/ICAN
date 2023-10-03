from typing import List, Dict, Tuple, Optional
from datetime import datetime
import openai
import yaml
import re


class Agent:
    def __init__(
        self,
        api_key: str,
        agent_context: str,
        model: str = "gpt-3.5-turbo",
        agent_name: str = "Agent",
    ) -> None:
        """
        Initialize the Agent class with API key, expertise, and model.

        Parameters:
            api_key (str): The OpenAI API key for making requests.
            agent_context (str): The root blueprint for this agent with his expertise.
            model (str, optional): The OpenAI model to use. Defaults to "gpt-3.5-turbo".
            agent_name (str, optional): The name of the agent. Defaults to "Agent".
        """
        self.api_key = api_key
        self.model = model
        self.agent_context = agent_context
        self.history: List[Dict[str, str]] = []
        self.previous_answers: List[Dict[str, str]] = []
        self.agent_name = agent_name
        self.agent_expertise = self.extract_expertise()

    def __str__(self) -> str:
        """
        Provide a string representation of the Agent instance.

        Returns:
            str: A string representation.
        """
        return f"Agent(Name: {self.agent_name}, Expertise: {self.agent_expertise}, Context: {self.agent_context}, Role: {self.role})"

    def extract_expertise(self) -> str:
        """
        Extract expertise from agent_context.

        Returns:
            str: The extracted expertise.
        """
        match = re.search(r"\n\s*(.*?):", self.agent_context)
        return match.group(1).strip() if match else "Unknown"

    def chat_completion(self, prompt: str) -> Tuple[str, Dict[str, str]]:
        """
        Perform chat completion using OpenAI API based on the given prompt and context history.

        Parameters:
            prompt (str): The user input or prompt for the agent to respond to.

        Returns:
            Tuple[str, Dict[str, str]]: A tuple containing the message output and the full message details.
        """
        openai.api_key = self.api_key
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": self.agent_context}],
        }

        if self.history:
            payload["messages"].extend(self.history)

        payload["messages"].append({"role": "user", "content": prompt})

        try:
            response = openai.ChatCompletion.create(**payload)
            message_output = response["choices"][0]["message"]["content"]
            return message_output, response["choices"][0]["message"]
        except Exception as e:
            raise Exception(f"Error: {e}")

    def listen(self, shared_history: List[Dict[str, str]]) -> None:
        """
        Update the agent's history based on the shared conversation history.

        Parameters:
            shared_history (List[Dict[str, str]]): The shared conversation history among all agents and the user.

        Returns:
            None
        """
        self.history = shared_history.copy()

    def reply(self) -> Tuple[str, Dict[str, str]]:
        """
        Generate a reply based on the agent's history and expertise.

        Returns:
            Tuple[str, Dict[str, str]]: A tuple containing the message output and the full message details.
        """
        last_prompt = self.history[-1]["content"] if self.history else ""
        message_output, full_output = self.chat_completion(last_prompt)
        new_entry = {"role": "assistant", "content": message_output}
        self.history.append(new_entry)
        self.previous_answers.append(
            {
                "answer": message_output,
                "prompt": last_prompt,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "round": len(self.previous_answers) + 1,
            }
        )

        return message_output, new_entry

    def get_previous_answers(self) -> List[Dict[str, str]]:
        """
        Retrieve the list of previous answers provided by this agent with additional context.

        Returns:
            List[Dict[str, str]]: A list containing dictionaries with all previous answers and their context from this agent.
        """
        return self.previous_answers
