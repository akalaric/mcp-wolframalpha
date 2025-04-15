import asyncio
from src.models.gemma_client import GemmaClient

if __name__ == "__main__":
    async def main():
        async with GemmaClient() as client:
            while True:
                user_input = await asyncio.to_thread(input, "Enter question (or type 'exit' to quit): ")
                if user_input.lower() == "exit":
                    print("Exiting...")
                    break
                response = await client.invokeModel(user_input)
                print(response.content)
    asyncio.run(main())