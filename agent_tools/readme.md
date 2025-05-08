# Agent Tools Framework

## Overview
This project provides a framework for building and running agents using Groq and various tools such as currency conversion, weather information retrieval, and web search via Tavily. The framework is designed to be modular, extensible, and easy to use.

---

## Features
- **Tool Integration**: Includes tools like `convert_currency`, `get_weather`, and `Tavily-based web search.`
- **Modular Design**: Easily add or modify tools and agents.
- **Groq Integration**: Leverages Groq for agent orchestration and execution.
- **Customizable Prompts**: Define system prompts and instructions for agents.

## Folder Structure
```
agent_tools/
├── src/
│   ├── tool_registry.py  # Tool registration and metadata
│   ├── tools.py          # Tool definitions (e.g., currency conversion, weather)
├── main.py               # Main script to run the agent framework
├── readme.md             # Documentation for the agent tools
```

## How to Run
1. Run the Agent Framework
Navigate to the agent_tools directory and run the main script:
    ```bash
    cd agent_tools

    uv run main.py
    ```

2. Example Queries
The framework supports queries like:
- "Convert 100 USD to EUR"
- "What is the weather in Tokyo today?"
- "I have 100000 IDR, how much JPY will I get?"
- "Search article about traveling to Japan"