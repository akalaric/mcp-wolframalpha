import os
import sys
import asyncio
import gradio as gr
from itertools import zip_longest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.googleGenerativeAI_client import GemmaClient
dir_path = os.path.dirname(os.path.realpath(__file__))
favicon_path = os.path.join(dir_path, 'wolfram-alpha.png')
client = None

async def startup():
    global client
    client = GemmaClient()
        
async def stream_response(response):
    partial = ""
    if not hasattr(response, "content") or not isinstance(response.content, str):
        return
    for line in response.content.splitlines():
        partial += line + "\n"
        await asyncio.sleep(0.1)
        yield {"role": "assistant", "content": partial}

async def google_generative_ai(messages, chatbot, history):
    chatHistory = chatbot if history else None
    response = await client.interact(messages, chatHistory)
    async for chunk in stream_response(response):
        yield chunk

async def wolfram_response_fn(messages, chatbot, history):
    chatHistory = chatbot if history else None
    response = await client.invoke_model(messages, chatHistory, vision=True)
    async for chunk in stream_response(response):
        yield chunk
        
# Gradio interface
def create_app():
    with gr.Blocks(fill_height=True) as GenerativeAI:
        with gr.Sidebar(open=False, width=250):
            gr.Markdown("⚙️ LLM Parameters")
            history_checkbox = gr.Checkbox(label="History", info="Turn chat history on or off")
            gr.HTML(
                '<a href="/gemini" target="_blank" '
                'style="display:inline-block;padding:.5em 1.2em;'
                'background:#007bff;color:#fff;border-radius:6px;'
                'text-decoration:none;font-weight:600;">'
                'Chat with Gemini</a>'
            )

        gr.Markdown("# Wolfram|Alpha Generative AI")
        # ── CHAT INTERFACE ───────────────────────────────────────────────────────
        gr.ChatInterface(
            fn=wolfram_response_fn,
            type="messages",
            description="Interact with Wolfram|Alpha: Computational Intelligence with Google Generative AI",
            additional_inputs = [history_checkbox],
            autoscroll=True,
            autofocus=True,
            editable=True,
            stop_btn=True
        )
        GenerativeAI.load(startup)
    
    with GenerativeAI.route("/Gemini"):
        gr.Markdown("# Gemini-2.0-flash")
        # ── CHAT INTERFACE ────────────────────────────────────────────────────────
        gr.ChatInterface(
            fn=google_generative_ai,
            type="messages",
            description="Interact with Gemini-2.0-flash",
            additional_inputs = [history_checkbox],
            autoscroll=True,
            autofocus=True,
            editable=True,
            stop_btn=True
        )
        
    return GenerativeAI

if __name__ == "__main__":
    gradio_app = create_app()
    gradio_app.launch(favicon_path=favicon_path)