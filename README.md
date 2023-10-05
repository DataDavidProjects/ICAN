# I-CAN: Intelligent Collaborative Agents Network

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Framework](https://img.shields.io/badge/framework-micro--framework-green)](https://github.com/yourusername/aican)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-orange)](https://openai.com/)

<div align="center">
  <img src="./public/logo/ICAN.png" width="500">
</div>

## Description

I-CAN (Intelligent Collaborative Agents Network) is a micro-framework for simulating a collaborative multi-agent system.
Each agent specializes in a particular domain and they work together to suggest the best way to solve a business problems.

The project is under development and feedbacks are welcome.

## 🚀 Features

- **Recruitment Agent**: Enables an HR-created agent to suggest the best expertise to work in tandem given the problem.
- **Multi-Agent Collaboration**: Enables multiple agents to work in tandem, offering holistic solutions.
- **Domain Specialization**: Each agent is an expert in its domain, ensuring expert solutions.
- **Brainstorming Sessions**: Agents can brainstorm to refine and enhance their suggestions.
- **Secretary Agent**: Enables to summarize the different proposed solutions by the BrainstormingSession.
- **Integrated with OpenAI GPT-3.5-turbo**: Leveraging OPENAI API.
- **Shared History**: Agents have access to shared conversation history, enabling informed decision-making.

## 🔧 Installation & Setup

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

Modify the business request and the context of agents using the config.yaml file

```
assistant:
  context: |
    .\n
    You will try to solve the problem and follow your area of expertise to improve and validate the different propositions of your peers.
    Express yourself professionally and avoid unnecessary talks.
    At each interaction you primary goal is to improve the previous answer.

user:
  request: |
    How can i find a remote job in Data Science ?
    provide me bullet point to do list.
```
