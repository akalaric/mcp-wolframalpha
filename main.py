import asyncio
import argparse
from src.models.gemma_client import GemmaClient
from src.ui import app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Invoke Gemma with query_wolfram MCP")
    parser.add_argument("--ui", action="store_true", help="Enable ui mode")
    args = parser.parse_args()
    
    async def main():
        async with GemmaClient() as client:
            while True:
                user_input = await asyncio.to_thread(input, "\nEnter question (or type 'exit' to quit): ")
                if user_input.lower() == "exit":
                    print("Exiting...")
                    break
                if not user_input.strip():
                    print("No input provided. Please enter a valid question.")
                    continue
                else:
                    response = await client.invokeModel(user_input)
                print(response.content)
                
    if args.ui:
        gradio_app = app.create_app()
        gradio_app.launch(favicon_path=app.favicon_path)
    else:
        asyncio.run(main())