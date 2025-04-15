import os
import sys
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.interface import baseFunctions
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler

class QuantizedLLM(baseFunctions):
    def __init__(self, model_path:str):
        try:
            callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
            self.llm = LlamaCpp(
                model_path=model_path,
                temperature=0.75,
                max_tokens=2000,
                top_p=1,
                callback_manager=callback_manager,
                verbose=True,  # Verbose is required to pass to the callback manager
                )
        except Exception as e:
            raise e
        super().__init__(self.llm)
        
        
# Test the client
if __name__ == "__main__":
    async def main():
        async with QuantizedLLM("Meta-Llama-3-8B-Instruct.Q4_K_M.gguf") as client:
            while True:
                user_input = await asyncio.to_thread(input, "Enter question (or type 'exit' to quit): ")
                if user_input.lower() == "exit":
                    print("Exiting...")
                    break
                response = await client.invokeModel(user_input)
                print(response.content)
        
    asyncio.run(main())