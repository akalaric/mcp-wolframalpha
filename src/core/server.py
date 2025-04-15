import mcp
import sys
import os
import asyncio
from fastmcp import FastMCP
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api.wolfram_client import WolframAlphaServer

mcp = FastMCP("WolframAlphaServer")
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
    try:
        wolfram_server = WolframAlphaServer()
    except Exception as e:
        raise Exception(f"Initialization error: {e}")
    sections = []
    results = await wolfram_server.execute_query(query)

    for item in results:
        if vision:
            if item.type == "text":
                sections.append({"type": "text", "text": item.text})
            elif item.type == "image":
                sections.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{item.mimeType};base64,{item.data}" 
                    }
                })
        else:
            if item.type == "text":
                print(item.text)
                sections.append({"type": "text", "text": item.text})
                    
    return sections if vision else "\n\n".join(item["text"] for item in sections)
    
if __name__ == "__main__":
    asyncio.run(mcp.run())
    
    