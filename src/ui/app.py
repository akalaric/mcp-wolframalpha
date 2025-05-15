import os
import sys
import asyncio
import gradio as gr
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.gemma_client import GemmaClient
dir_path = os.path.dirname(os.path.realpath(__file__))
favicon_path = os.path.join(dir_path, 'wolfram-alpha.png')
client = None 
async def startup():
    global client
    client = GemmaClient()
    await client.__aenter__()

async def shutdown():
    global client
    if client:
        await client.__aexit__(None, None, None)
        
# Exit button callback
def exit_app():
    GenerativeAI.close()
    return "App is shutting down..."

async def model_response_fn(messages, chatbot):
    global client
    response = await client.invokeModel(messages, vision=True)
    return response.content

# Gradio interface
def create_app():
    global GenerativeAI
    with gr.Blocks(fill_height=True) as GenerativeAI:
        gr.Markdown("# Wolfram|Alpha Generative AI\nInteract with Wolfram|Alpha: Computational Intelligence with Google Generative AI")

        chat = gr.ChatInterface(
            fn=model_response_fn,
            type="messages",
            title=None,
            description=None
        )
        

        GenerativeAI.load(startup)
        GenerativeAI.unload(shutdown)

    return GenerativeAI