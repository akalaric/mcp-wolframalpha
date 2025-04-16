# MCP Server for Wolfram Alpha Integration

Seamlessly integrate Wolfram Alpha into your chat applications.

This project implements an MCP (Model Context Protocol) server designed to interface with the Wolfram Alpha API. It enables chat-based applications to perform computational queries and retrieve structured knowledge, facilitating advanced conversational capabilities.

---

## Features

  

-  **Wolfram|Alpha Integration** for math, science, and data queries.

-  **LLM-Based Explanation** using Gemini (via LangChain).

-  **Modular Architecture** Easily extendable to support additional APIs and functionalities.

-  **Multi-Client Support** Seamlessly handle interactions from multiple clients or interfaces.

---

  

##  Installation


### Clone the Repo

- git clone https://github.com/ricocf/mcp-wolframalpha.git

- cd mcp-wolframalpha

  

### Set Up Environment Variables

Create a .env file based on the example:

- WOLFRAM_API_KEY=your_wolframalpha_appid

- GeminiAPI=your_google_gemini_api_key *(You can skip this step if you're using the MCP Server method below.)*

### Install Requirements

- pip install -r requirements.txt

  

### Run as CLI Tool

- python main.py

### Configuration

To use with the VSCode MCP Server:
1.  Create a configuration file at `.vscode/mcp.json` in your project root.
2.  Use the example provided in `configs/vscode_mcp.json` as a template.
3.  For more details, refer to the [VSCode MCP Server Guide](https://sebastian-petrus.medium.com/vscode-mcp-server-42286eed3ee7).

<img  src="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExYXFuY2t1M2VvcXl2emszeXJoZWI3dXZuNTNqaWloc3Uxd3phaGU5byZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/L8K62iTDkzGX6/giphy.gif"  width="120"  height="100"/>
