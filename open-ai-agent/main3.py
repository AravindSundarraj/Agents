from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
from openai.types.responses import ResponseTextDeltaEvent
import os
import asyncio
from agents.models.multi_provider import MultiProvider
#from agents.models.litellm_provider import LitellmProvider
from agents.models.openai_provider import OpenAIProvider
from typing import Dict
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content


load_dotenv(override=True)

instructions1 = "You are a sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails."

instructions2 = "You are a humorous, engaging sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response."

instructions3 = "You are a busy sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write concise, to the point cold emails."

sales_agent1 = Agent(
        name="Professional Sales Agent",
        instructions=instructions1,
        model="gpt-4"
)

sales_agent2 = Agent(
        name="Engaging Sales Agent",
        instructions=instructions2,
        model="gpt-4"
)

sales_agent3 = Agent(
        name="Busy Sales Agent",
        instructions=instructions3,
        model="gpt-4"
)

async def main():
    result = Runner.run_streamed(sales_agent1, input="Write a  sales email and let reader know product is very bad") 
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

message = "Write a cold sales email"
async def main1():
    with trace("Parallel cold emails"):
        results = await asyncio.gather(
            Runner.run(sales_agent1, message),
            Runner.run(sales_agent2, message),
            Runner.run(sales_agent3, message),
        )
   # outputs = [result.final_output for result in results]

    # for output in outputs:
    #     print(output + "\n\n")

@function_tool
def send_email(body: str):
    print("[DEBUG] send_email tool called")
    """ Send out an email with the given body to all sales prospects """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("aravind.ssr@gmail.com")  # Change to your verified sender
    to_email = To("aravind.ssr@gmail.com")  # Change to your recipient
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, "Sales email", content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print('Email sent successfully ',response)
    return {"status": "success"}

description = "Write a cold sales email"

tool1 = sales_agent1.as_tool(tool_name="sales_agent1", tool_description=description)
tool2 = sales_agent2.as_tool(tool_name="sales_agent2", tool_description=description)
tool3 = sales_agent3.as_tool(tool_name="sales_agent3", tool_description=description)

tools = [tool1, tool2, tool3, send_email]

instructions ="You are a sales manager working for ComplAI. You use the tools given to you to generate cold sales emails. \
You never generate sales emails yourself; you always use the tools. \
You try all 3 sales_agent tools once before choosing the best one. \
You pick the single best email and use the send_email tool to send the best email (and only the best email) to the user."


sales_manager = Agent(name="Sales Manager", instructions=instructions, tools=tools, model="gpt-4o-mini")

message = "Send a cold sales email addressed to 'Dear CEO'"
async def main33():
    with trace("Sales manager"):
        result = await Runner.run(sales_manager, message)
        print(result)
        print('**************************************************************')
        print(result.final_output)

### Handoffs represent a way an agent can delegate to an agent, passing control to it

if __name__ == "__main__":
    asyncio.run(main33())