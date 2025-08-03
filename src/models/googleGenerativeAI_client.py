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
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GeminiAPI environment variable not set")
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=api_key,
                streaming=True
            )
        except Exception as e:
            raise e
        super().__init__(self.llm) #invoke from the baseFunction
        

# Test the client
if __name__ == "__main__":
    async def main():
        client = GemmaClient()
        while True:
            user_input = await asyncio.to_thread(input, "Enter question (or type 'exit' to quit): ")
            if user_input.lower() == "exit":
                print("Exiting...")
                break
            response = await client.invoke_model(user_input, vision=True)
            print(response.content)
    asyncio.run(main())