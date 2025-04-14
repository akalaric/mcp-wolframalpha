import argparse
import asyncio
from src.models.gemma_client import GemmaClient, call_mcp_tool

async def main(query: str):
    try:
        mcp_response = await call_mcp_tool(query)
        gemma = GemmaClient()
        explanation = await gemma.generate(mcp_response)
        print(explanation.content)
    except Exception as e:
        raise RuntimeError("Error during MCP tool call") from e

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Invoke Gemma with query_wolfram MCP")
    parser.add_argument("query", type=str, help="Ask Wolfram|Alpha")
    args = parser.parse_args()
    asyncio.run(main(args.query))
