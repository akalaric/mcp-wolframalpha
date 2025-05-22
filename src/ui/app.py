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

async def model_response_fn(messages, chatbot, history, GenAI):
    chatHistory = None
    if history:
        chatHistory = chatbot
    if GenAI:
        response = await client.interact(messages, chatHistory)
    else:
        response = await client.invokeModel(messages, chatHistory, vision=False)
        
    partial = ""
    for line in response.content.splitlines():
        partial += line + "\n"
        await asyncio.sleep(0.1)
        yield {"role": "assistant", "content": partial}

# Gradio interface
def create_app():
    with gr.Blocks(fill_height=True) as GenerativeAI:
        with gr.Sidebar(open=False):
            gr.Markdown("⚙️ LLM Parameters")
            additional_inputs=[
            gr.Checkbox(label="History", info="Turn chat history on or off"),
            gr.Checkbox(label="Google Generative AI", info="Interact with Google Generative AI"),
        ]
            
        gr.Markdown("# Wolfram|Alpha Generative AI")
        gr.ChatInterface(
            fn=model_response_fn,
            type="messages",
            description="Interact with Wolfram|Alpha: Computational Intelligence with Google Generative AI",
            additional_inputs=additional_inputs,
            autoscroll=True,
            autofocus=True,
            editable=True,
        )
        GenerativeAI.load(startup)
        GenerativeAI.unload(shutdown)

    return GenerativeAI