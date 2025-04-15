from langchain.prompts import ChatPromptTemplate
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
            wolfram_response = ", ".join(item.text for item in result)
        except Exception as e:
            raise RuntimeError("Error during MCP tool call") from e
        
        if wolfram_response:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a brilliant scientific assistant who excels at breaking down concepts into clear explanations. If any visual information is included, explain and show the content"),
                ("human", "Here's the result: {wolfram_response}. Can you explain  it?"),
            ])
            chain = prompt | self.generator
            response = chain.invoke({"wolfram_response": wolfram_response})
        else:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a knowledgeable scientific assistant. Provide a straightforward and simple explanation for the following question."),
                ("human", "Here’s a question: {wolfram_response}. Can you break it down and provide a simple answer?"),
            ])
            chain = prompt | self.generator
            response = chain.invoke({"wolfram_response": query})
        
        return response
