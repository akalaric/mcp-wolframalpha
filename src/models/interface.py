from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from fastmcp import Client

class baseFunctions:
    def __init__(self, generator, server_path="src/core/server.py"):
        self.generator = generator
        self.server_path = server_path
        self.client = None

    async def __aenter__(self):
        self.client = await Client(self.server_path).__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.__aexit__(exc_type, exc_value, traceback)
        
    async def interact(self, query:str, history=None):
        messages = [
            SystemMessage(content=("You are a brilliant scientific assistant who explains concepts clearly and concisely. "))]
        if history:
            for msg in history:
                role = msg.get("role")
                content = msg.get("content")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))

        messages.append(HumanMessage(content=query))
        response = await self.generator.ainvoke(messages)
        return response

    async def invokeModel(self, query, history=None, vision=False):
        try:
            result = await self.client.call_tool("query_wolfram", {"query": query, "vision": vision})
        except Exception as e:
            raise RuntimeError("Error during MCP tool call") from e

        prompt_content = []
        if result:
            for section in result:
                if hasattr(section, "type") and section.type == "text":
                    prompt_content.append(section.text)
                elif hasattr(section, "type") and section.type == "image" and vision:
                     prompt_content.append(f"[Image URL]({section.data})")
                     
        # Fallback if no useful content
        if all(isinstance(item, str) and not item.strip() for item in prompt_content):
            fallback_message = "There was no result from Wolfram Alpha for this query:."
            prompt_content.append(f"{fallback_message}\n\n{query}")

        messages = [
                    SystemMessage(
                        content=(
                            "You are a brilliant scientific assistant who explains concepts clearly and concisely. "
                            "If visual input (like images) is available, include it as a Markdown image: `![description](URL)`. "
                            "Do not omit the image. Always include the image URL visibly using Markdown format. "
                            "Explain the content clearly, and if an image is present, refer to it directly in your explanation."
                        )
                    )]
        messages.append(HumanMessage(content="\n\n".join(prompt_content)))
        if history:
            for msg in history:
                role = msg.get("role")
                content = msg.get("content")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
                    
        response = await self.generator.ainvoke(messages)  
        return response
