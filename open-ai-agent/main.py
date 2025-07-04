from dotenv import load_dotenv
import asyncio
from agents import Agent, Runner, trace
from openai import OpenAI
import os # Requires: pip install -U langchain-openai

# Load API key from .env
load_dotenv(override=True)



# # Initialize the model using LangChain-OpenAI wrapper
# llm = ChatOpenAI(
#     model="gpt-4o",  # openrouter supports gpt-4o
#     temperature=0.7,
#     base_url=os.environ["OPENAI_API_BASE"]
# )
agent = Agent(name="Jokester", instructions="You are a joke teller", model="gpt-4o-mini")



# Async runner function
async def main():
    # Run the joke with Runner.run(agent, prompt) then print final_output

 with trace("Telling a joke"):
    result = await Runner.run(agent, "Tell a joke about Autonomous AI Agents")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
