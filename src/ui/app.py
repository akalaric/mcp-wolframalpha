import os
import sys
import asyncio
import gradio as gr
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.gemma_client import GemmaClient


async def GoogleGenerativeAI(input_text, vision=True):
    async with GemmaClient() as generator_instance:
        response = await generator_instance.invokeModel(input_text, vision)
        return response.content


generator_interface = gr.ChatInterface(GoogleGenerativeAI, type="messages", title="Wolfram|Alpha Generative AI", description="Interact with Wolfram|Alpha: Computational Intelligence with Google Generative AI")

dir_path = os.path.dirname(os.path.realpath(__file__))
favicon_path = os.path.join(dir_path, 'wolfram-alpha.png')

generator_interface.launch(favicon_path=favicon_path)