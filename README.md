# 🚧 MCP WolframAlpha

Model-Context-Protocol (MCP) tool that queries **Wolfram|Alpha**, processes structured results (text/images), and explains them using an LLM model via **LangChain**. It includes a CLI entrypoint and a FastMCP server.

---

## ✨ Features

- 📡 **Wolfram|Alpha Integration** for math, science, and data queries  
- 🧠 **LLM-Based Explanation** using Gemini (via LangChain)  
- 🖼️ Optional **vision support**: returns base64-encoded images  
- ⚡ Fully async architecture for scalable tool calls  

---

## ⚙️ Installation

### 1. Clone the Repo
- git clone https://github.com/ricocf/mcp-wolframalpha.git
- cd mcp-wolframalpha

### 2. Set Up Environment Variables
Create a .env file based on the example:
- WOLFRAM_API_KEY=your_wolframalpha_appid
- GeminiAPI=your_google_gemini_api_key

### 3. Install Requirements
- pip install -r requirements.txt

### 4. 🚀 Run as CLI Tool
- python main.py
 
 
