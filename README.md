# Tool Generator Agent

## Overview

The **Tool Generator Agent** is an advanced AI system designed to automate the creation of function-calling tools for Large Language Models (LLMs) using OpenAI's Assistant API. The agent enables the generation, testing, and deployment of tools based on user prompts, streamlining the process of tool development.

This agent not only creates tools but also includes a feedback mechanism to correct errors in real-time, an automatic unit test generator to ensure tool reliability across edge cases, and an iterative development process to refine tools until they meet all requirements. The generated tools are stored in a knowledge base, which the agent queries using cosine similarity to retrieve existing tools that closely match new requests.

## Key Features

- **Automated Tool Creation**: Generates tools for LLMs from user prompts using OpenAI's Assistant API.
- **Feedback Loop**: The agent self-corrects during tool creation by detecting and fixing errors, ensuring high-quality output.
- **Automatic Unit Test Generation**: Creates unit tests to cover edge cases, refining the tool through iterative development until it passes all tests.
- **Knowledge Base with Similarity Search**: Stores all generated tools and uses cosine similarity to retrieve existing tools based on new prompts, avoiding redundant tool creation.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/tool-generator-agent.git
   cd tool-generator-agent
   ```

2. **Install Required Packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the agent with the following command:

```bash
python main.py
```

## Usage

- **Tool Generation**: Provide a prompt describing the tool you need, and the agent will generate it, test it, and refine it if necessary.
- **Tool Retrieval**: If a similar tool already exists in the knowledge base, the agent will retrieve and return it instead of creating a new one.

## Example

**Prompt**: "Create a tool that fetches current weather data for a given city."

**Output**: A Python function that interacts with a weather API, retrieves data, and returns a structured summary.
