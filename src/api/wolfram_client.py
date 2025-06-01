import os
import sys
from dotenv import load_dotenv
import wolframalpha
import aiohttp
import asyncio
import base64
from dataclasses import dataclass
from typing import Union
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

@dataclass
class TextContent:
    type: str
    text: str

@dataclass
class ImageContent:
    type: str
    data: str  # URL
    mimeType: str

ResultType = Union[TextContent, ImageContent]

class WolframAlphaServer:
    def __init__(self):
        api_key = os.getenv("WOLFRAM_API_KEY")
        if api_key is None:
            raise ValueError("WOLFRAM_API_KEY environment variable not set")
        try:
            self.client = wolframalpha.Client(api_key)
        except Exception as e:
            raise e
        
    async def process_query(self, query: str) -> list[ResultType]:
        """Main query execution method"""
        try:
            res = await self.client.aquery(str(query))
            return await self.process_results(res)
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]

    async def process_results(self, res) -> list[ResultType]:
        """Process results into text/image formats"""
        results: list[ResultType] = []
        try:
            for pod in res.pods:
                for subpod in pod.subpods:
                    if subpod.get("plaintext"):
                        results.append(TextContent(
                            type="text",
                            text=subpod.plaintext
                        ))
                    elif subpod.get("img"):
                        img_src = subpod["img"]["@src"]
                        results.append(ImageContent(
                            type="image",
                            data=img_src,  # store URL directly
                            mimeType="image/png"
                        ))
        except Exception as e:
            raise Exception("Failed to parse response from Wolfram Alpha") from e
        return results

# Test the client
if __name__ == "__main__":
    async def main():
        test = WolframAlphaServer()
        result = await test.process_query("sin(x)*cos(x)")
        for item in result:
            if item.type == "text":
                print (item.text)
            if item.type == "image":
                print(item.data)
    asyncio.run(main())
