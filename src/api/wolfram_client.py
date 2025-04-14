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
    data: str  # base64 encoded
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

    async def execute_query(self, query: str) -> list[ResultType] | str:
        """Main query execution method"""
        try:
            res = await asyncio.to_thread(self.client.query, query)
        except Exception as e:
            return f"Error: {str(e)}"
        return await self.process_results(res)

    async def process_results(self, res) -> list[ResultType]:
        """Process results into text/image formats"""
        results: list[ResultType] = []

        try:
            async with aiohttp.ClientSession() as session:
                for pod in res.pods:
                    for subpod in pod.subpods:
                        if subpod.get("plaintext"):
                            results.append(TextContent(
                                type="text",
                                text=subpod.plaintext
                            ))
                        elif subpod.get("img"):
                            img_url = subpod.img.src if subpod.img else None
                            if img_url:
                                image_data = await self.fetch_image(session, img_url)
                                if image_data:
                                    results.append(ImageContent(
                                        type="image",
                                        data=image_data,
                                        mimeType="image/png"
                                    ))
        except Exception as e:
            raise Exception("Failed to parse response from Wolfram Alpha") from e
        return results

    async def fetch_image(self, session: aiohttp.ClientSession, url: str) -> str | None:
        """Download and encode image from URL"""
        try:
            async with session.get(url) as img_response:
                if img_response.status == 200:
                    img_bytes = await img_response.read()
                    return base64.b64encode(img_bytes).decode("utf-8")
        except Exception as e:
            print(f"Image fetch error: {e}")
        return None

    async def concurrent_queries(self, *queries):
        """Handle multiple queries simultaneously"""
        tasks = [self.execute_query(q) for q in queries]
        return await asyncio.gather(*tasks)
    
# Test the client
if __name__ == "__main__":
    async def main():
        test = WolframAlphaServer()
        result = await test.execute_query("1+1")
        for item in result:
            if item.type == "text":
                print (item.text)

    asyncio.run(main())
