import os
import sys
import asyncio
from fastmcp import Client
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

async def call_mcp_tool(input_data, vision=False) -> str:
    try:
        async with Client("src/core/server.py") as client:
            # tools = await client.list_tools()
            result = await client.call_tool("query_wolfram", {"query": input_data, "vision":vision})
            # result = await client.call_tool("query_wolfram", {"query": input_data})
            return ", ".join(item.text for item in result)
    except Exception as e:
        raise RuntimeError("Error during MCP tool call") from e

class GemmaClient:
    def __init__(self):
        api_key = os.getenv("GeminiAPI")
        if not api_key:
            raise ValueError("GeminiAPI environment variable not set")
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=api_key
        )

    async def generate(self, wolfram_response) -> str:
        prompt = f"""You are an expert assistant.
        Here is data from WolframAlpha:
        {wolfram_response}
        Please explain this data in simple terms."""
        return await self.llm.ainvoke(prompt)

# Test the client
async def main():
    print(await call_mcp_tool("Y = -X"))

if __name__ == "__main__":
    asyncio.run(main())
