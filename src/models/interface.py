from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from fastmcp import Client
import json

class baseFunctions:
    def __init__(self, generator, server_path="src/core/server.py"):
        self.generator = generator
        self.server_path = server_path
        
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

    async def invoke_model(self, query, history=None, vision=False):
        try:
            async with Client(self.server_path) as client:
                result = await client.call_tool("query_wolfram", {"query": query, "vision": vision})
        except Exception as e:
            raise RuntimeError(f"Error during MCP tool call: {e}")
        prompt_content = []
        
        if result:
            for text_content in result.content:
                    items = json.loads(text_content.text)
                    for item in items:
                        if item.get("type") == "text":
                            prompt_content.append(item["text"])

        # Fallback if no useful content
        if all(isinstance(item, str) and not item.strip() for item in prompt_content):
            fallback_message = "There was no result from Wolfram Alpha for this query:."
            prompt_content.append(f"{fallback_message}\n\n{query}")

        messages = [
                    SystemMessage(
                            content = (
                                """
                                You are a knowledgeable and articulate scientific assistant with a strong ability to communicate complex scientific and mathematical concepts in a clear, concise, and accessible manner.

                                **You must always display image URLs using Markdown image syntax**, like this:
                                ![Alt text](https://example.com/image.png)

                                ❗ No exceptions — all image URLs must be embedded as Markdown images, whether they appear in the body of your explanation, in image references, or at the end of your response. Do not output plain image URLs.

                                Your explanations should be accurate, detailed, well-structured, and tailored to the level of the audience, making even advanced topics easy to grasp.

                                When an image, graph, or diagram is provided, you must reference it directly in your explanation, using it to support and enrich your analysis. Highlight key features, trends, or relationships shown in the image to reinforce understanding.

                                Your goal is to educate effectively, ensuring that the explanation is both insightful and engaging.
                                """
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
