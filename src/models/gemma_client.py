import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from models.interface import baseFunctions
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class GemmaClient(baseFunctions):
    def __init__(self):
        api_key = os.getenv("GeminiAPI")
        if not api_key:
            raise ValueError("GeminiAPI environment variable not set")
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=api_key
            )
        except Exception as e:
            raise e
        super().__init__(self.llm) #invoke from the baseFunction
        

# Test the client
if __name__ == "__main__":
    async def main():
        async with GemmaClient() as client:
            while True:
                test = input("Enter question: ")
                response = await client.invokeModel(test)
                print(response.content)

    asyncio.run(main())

