from operator import truediv
from langgraph.prebuilt import create_react_agent
import getpass
import os
import asyncio

from dotenv import load_dotenv

load_dotenv(override=True)
# Define tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# Create ReAct agent
agent = create_react_agent(
    model="openai:gpt-4o",
    tools=[get_weather],
    prompt="You are a helpful assistant."
)

# Run the agent
async def main():
    result = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": "What is the weather in San Francisco?"}
        ]
    })
    print("DEBUG:", result) 
    print('**************************************************************')
    print(result["messages"][-1].content)

    # print(result["messages"][-1]["content"])

if __name__ == "__main__":
    asyncio.run(main())