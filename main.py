import asyncio
import argparse
from src.models.googleGenerativeAI_client import GemmaClient
from src.ui import app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Invoke Gemma with query_wolfram MCP")
    parser.add_argument("--ui", action="store_true", help="Enable ui mode")
    parser.add_argument("--model", action="store_true", help="Interact with Google Generative AI")
    args = parser.parse_args()
    
    async def main():
        client = GemmaClient()
        while True:
            user_input = await asyncio.to_thread(input, "\nEnter question (or type 'exit' to quit): ")
            if user_input.lower() == "exit":
                print("Exiting...")
                break
            elif not user_input.strip():
                print("No input provided. Please enter a valid question.")
                continue
            elif args.model:
                response = await client.interact(user_input)
            else:
                response = await client.invoke_model(user_input, vision=True)
            print(response.content)
            
    if args.ui:
        gradio_app = app.create_app()
        gradio_app.launch(favicon_path=app.favicon_path)
    else:
        asyncio.run(main())