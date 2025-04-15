import asyncio
import argparse
from src.models.gemma_client import GemmaClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Invoke Gemma with query_wolfram MCP")
    parser.add_argument("--vision", action="store_true", help="Enable vision mode")
    args = parser.parse_args()
    
    async def main():
        async with GemmaClient() as client:
            while True:
                user_input = await asyncio.to_thread(input, "\nEnter question (or type 'exit' to quit): ")
                if user_input.lower() == "exit":
                    print("Exiting...")
                    break
                if args.vision:
                    response = await client.invokeModel(user_input, vision=True)
                else:
                    response = await client.invokeModel(user_input)
                print(response.content)
    asyncio.run(main())