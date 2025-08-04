import os
import sys
import asyncio
import logging
from typing import Union
from pydantic import BaseModel
import xmltodict, multidict, httpx
from wolframalpha import Client, Document
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()

class TextContent(BaseModel):
    type: str
    text: str

class ImageContent(BaseModel):
    type: str
    data: str 
    mimeType: str

ResultType = Union[TextContent, ImageContent]
logging.basicConfig(level=logging.INFO)

class WolframAlphaServer:
    def __init__(self):
        api_key = os.getenv("WOLFRAM_API_KEY")
        if api_key is None:
            raise ValueError("WOLFRAM_API_KEY environment variable not set")
        try:
            self.client = Client(api_key)
        except Exception as e:
            raise e
        
    async def process_query(self, query: str) -> list[ResultType]:
        """Main query execution method"""
        try:
            res = await self.client.aquery(str(query))
            return await self.process_results(res)
        except Exception:
            logging.warning("Wolfram|Alpha lib assertion error -> Using manual API call")
            timeout = httpx.Timeout(30.0, read=30.0)
            params = {
                "appid": self.client.app_id,
                "input": str(query)
            }
            res = None
            max_retries = 4
            for attempt in range(1, max_retries + 1):
                try:
                    async with httpx.AsyncClient(timeout=timeout) as client:
                        resp = await client.get(self.client.url, params=params)
                        res = xmltodict.parse(resp.content, postprocessor=Document.make)['queryresult']
                        if res:
                            return await self.process_results(res)
                except Exception as e:
                    logging.warning(f"Attempt {attempt} failed: {e}. Retrying in 2s...")
                await asyncio.sleep(2)
            raise RuntimeError("Failed to get a valid response from WolframAlpha API after several retries.")

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
        result = await test.process_query("sinx")
        for item in result:
            if item.type == "text":
                print (item.text)
            if item.type == "image":
                print(item.data)
    asyncio.run(main())
