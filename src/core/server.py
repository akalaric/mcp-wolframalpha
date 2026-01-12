import sys
import os
import asyncio
import logging
from fastmcp import FastMCP
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.wolfram_client import WolframAlphaServer

mcp = FastMCP("WolframAlphaServer")

try:
    wolfram_server = WolframAlphaServer()
except Exception as e:
    logging.error(f"Error initializing WolframServer: {e}", file=sys.stderr)
    sys.exit(1)


@mcp.tool(name="query_wolfram")
async def wolfram_query(query: str, vision=False):
    """
    Query the WolframAlpha API with a natural language input.

    Args:
        query (str): The natural language query to send to WolframAlpha.
        vision (bool): Whether to include images (for vision-capable LLMs).

    Returns:
        Union[str, list]: Formatted string or structured message list.
    """
    results = await wolfram_server.process_query(query)

    sections = []
    for item in results:
        if vision:
            if hasattr(item, 'type'):
                if item.type == "text":
                    sections.append({"type": "text", "text": item.text})
                elif item.type == "image":
                    sections.append({
                        "type": "image",
                        "url": item.data  # direct URL
                    })
            elif isinstance(item, str):
                sections.append({"type": "text", "text": item})
        else:
            if hasattr(item, 'type'):
                if item.type == "text":
                    sections.append({"type": "text", "text": item.text})
            elif isinstance(item, str):
                sections.append({"type": "text", "text": item})

    return sections if vision else "\n\n".join(item["text"] for item in sections)
        
if __name__ == "__main__":
    
    # Test the server
    # async def main():
    #     async with Client(mcp) as client:
    #         result = await client.call_tool("query_wolfram", {"query": "sinx", "vision": True})
    #     print(result)   
        
    # asyncio.run(main())
    
    mcp.run()
    
    
