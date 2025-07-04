import os
import asyncio
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI  # Requires: pip install -U langchain-openai

# Load API key from .env
load_dotenv(override=True)



# # Initialize the model using LangChain-OpenAI wrapper
# llm = ChatOpenAI(
#     model="gpt-4o",  # openrouter supports gpt-4o
#     temperature=0.7,
#     base_url=os.environ["OPENAI_API_BASE"]
# )
agent = create_react_agent(
    model="openai:gpt-4o",
    tools=[],
    prompt="You are a joke teller."
)



# Async runner function
async def main():
    result = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": "Tell a joke about Autonomous AI Agents"}
        ]
    })
    print("🤖 Joke:", result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
