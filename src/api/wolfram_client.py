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
        except AssertionError as ae:
            logging.warning("wolframalpha library’s assertion error -> Using manual API call")
            timeout = httpx.Timeout(50.0, read=50.0)
            params = {
                "appid": self.client.app_id,
                "input": str(query)
            }

            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.get(self.client.url, params=params)
            res = xmltodict.parse(resp.content, postprocessor=Document.make)['queryresult']
            
        except Exception as e:
            logging.exception("Unexpected error during query processing")
            raise e
        
        return await self.process_results(res)

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
        while True:
            result = await test.process_query("sin(x)")
            for item in result:
                if item.type == "text":
                    print (item.text)
                if item.type == "image":
                    print(item.data)
    asyncio.run(main())
