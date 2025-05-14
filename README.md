[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/ricocf-mcp-wolframalpha-badge.png)](https://mseep.ai/app/ricocf-mcp-wolframalpha)

# MCP Wolfram Alpha (Client + Server)
Seamlessly integrate Wolfram Alpha into your chat applications.

This project implements an MCP (Model Context Protocol) server designed to interface with the Wolfram Alpha API. It enables chat-based applications to perform computational queries and retrieve structured knowledge, facilitating advanced conversational capabilities.

Included is an MCP-Client example utilizing Gemini via LangChain, demonstrating how to connect large language models to the MCP server for real-time interactions with Wolfram Alpha’s knowledge engine.

---

## Features

-  **Wolfram|Alpha Integration** for math, science, and data queries.

-  **Modular Architecture** Easily extendable to support additional APIs and functionalities.

-  **Multi-Client Support** Seamlessly handle interactions from multiple clients or interfaces.

-  **MCP-Client example** using Gemini (via LangChain).

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

   

