from langchain_core.messages import SystemMessage, HumanMessage
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

    async def invokeModel(self, query, vision=False):
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
                    image_data_uri = f"data:{section.mimeType};base64,{section.data}"
                    prompt_content.append({
                        "type": "image_url",
                        "image_url": {"url": image_data_uri}
                    })
        if all(isinstance(item, str) and not item.strip() for item in prompt_content):
            fallback_message = "There was no result from Wolfram Alpha for this query:."
            prompt_content.append(f"{fallback_message}\n\n{query}")

        messages = [
            SystemMessage(
                content=(
                    "You are a brilliant scientific assistant who explains concepts clearly and concisely. "
                    "If visual input (like images) is available, use it to enhance your explanation. "
                    "Avoid generating LaTeX diagrams, TikZ, or PGFPlots code. "
                    "Instead, explain the content in words or refer to the image directly."
                )),
            HumanMessage(content=prompt_content)
        ]
        response = await self.generator.ainvoke(messages)
        return response
