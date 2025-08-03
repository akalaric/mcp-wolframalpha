# MCP Wolfram Alpha (Server + Client)
Seamlessly integrate Wolfram Alpha into your chat applications.

This project implements an MCP (Model Context Protocol) server designed to interface with the Wolfram Alpha API. It enables chat-based applications to perform computational queries and retrieve structured knowledge, facilitating advanced conversational capabilities.

Included is an MCP-Client example utilizing Gemini via LangChain, demonstrating how to connect large language models to the MCP server for real-time interactions with Wolfram Alpha’s knowledge engine.

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/akalaric/mcp-wolframalpha)
---

## Features

-  **Wolfram|Alpha Integration** for math, science, and data queries.

-  **Modular Architecture** Easily extendable to support additional APIs and functionalities.

-  **Multi-Client Support** Seamlessly handle interactions from multiple clients or interfaces.

-  **MCP-Client example** using Gemini (via LangChain).
-  **UI Support** using Gradio for a user-friendly web interface to interact with Google AI and Wolfram Alpha MCP server.

---

##  Installation


### Clone the Repo
   ```bash
   git clone https://github.com/ricocf/mcp-wolframalpha.git

   cd mcp-wolframalpha
   ```
  

### Set Up Environment Variables

Create a .env file based on the example:

- WOLFRAM_API_KEY=your_wolframalpha_appid

- GeminiAPI=your_google_gemini_api_key *(Optional if using Client method below.)*

### Install Requirements
   ```bash
   pip install -r requirements.txt
   ```

  Install the required dependencies with uv:
  Ensure [`uv`](https://github.com/astral-sh/uv) is installed.

   ```bash
   uv sync
   ```

### Configuration

To use with the VSCode MCP Server:
1.  Create a configuration file at `.vscode/mcp.json` in your project root.
2.  Use the example provided in `configs/vscode_mcp.json` as a template.
3.  For more details, refer to the [VSCode MCP Server Guide](https://sebastian-petrus.medium.com/vscode-mcp-server-42286eed3ee7).

To use with Claude Desktop:
```json
{
  "mcpServers": {
    "WolframAlphaServer": {
      "command": "python3",
      "args": [
        "/path/to/src/core/server.py"
      ]
    }
  }
}
```
## Client Usage Example

This project includes an LLM client that communicates with the MCP server.

#### Run with Gradio UI
- Required: GeminiAPI
- Provides a local web interface to interact with Google AI and Wolfram Alpha.
- To run the client directly from the command line:
```bash
python main.py --ui
```
#### Docker
To build and run the client inside a Docker container:
```bash
docker build -t wolframalphaui -f .devops/ui.Dockerfile .

docker run wolframalphaui
```
#### UI
- Intuitive interface built with Gradio to interact with both Google AI (Gemini) and the Wolfram Alpha MCP server.
- Allows users to switch between Wolfram Alpha, Google AI (Gemini), and query history.
  
![UI](configs/gradio_ui.png)

#### Run as CLI Tool
- Required: GeminiAPI
- To run the client directly from the command line:
```bash
python main.py
```
#### Docker
To build and run the client inside a Docker container:
```bash
docker build -t wolframalpha -f .devops/llm.Dockerfile .

docker run -it wolframalpha
```

## Contact

Feel free to give feedback. The e-mail address is shown if you execute this in a shell:

```sh
printf "\x61\x6b\x61\x6c\x61\x72\x69\x63\x31\x40\x6f\x75\x74\x6c\x6f\x6f\x6b\x2e\x63\x6f\x6d\x0a"
```

