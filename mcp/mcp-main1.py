from dotenv import load_dotenv
from agents import Agent, Runner, trace, RunResult
from agents.mcp import MCPServerStdio
import os
import logging
load_dotenv(override=True)
fetch_params = {"command": "uvx", "args": ["mcp-server-fetch"]}

async with MCPServerStdio(params=fetch_params, client_session_timeout_seconds=30) as server:
    fetch_tools = await server.list_tools()

fetch_tools

playwright_params = {"command": "npx","args": [ "@playwright/mcp@latest"]}

async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=30) as server:
    playwright_tools = await server.list_tools()

playwright_tools

sandbox_path = os.path.abspath(os.path.join(os.getcwd(), "sandbox"))
files_params = {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", sandbox_path]}

async with MCPServerStdio(params=files_params,client_session_timeout_seconds=30) as server:
    file_tools = await server.list_tools()

file_tools
instructions = """
You browse the internet to accomplish your instructions.
You are highly capable at browsing the internet independently to accomplish your task, 
including accepting all cookies and clicking 'not now' as
appropriate to get to the content you need. If one website isn't fruitful, try another. 
Be persistent until you have solved your assignment,
trying different options and sites as needed.
"""


async with MCPServerStdio(params=files_params, client_session_timeout_seconds=30) as mcp_server_files:
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("httpx").setLevel(logging.INFO)
    logging.getLogger("agents").setLevel(logging.DEBUG)
    logging.info("Starting MCP server for files")
    async with MCPServerStdio(params=playwright_params, client_session_timeout_seconds=30) as mcp_server_browser:
        logging.info("Starting MCP server for files - 222")
        agent = Agent(
            name="investigator", 
            instructions=instructions, 
            model="gpt-4.1-mini",
            mcp_servers=[mcp_server_files, mcp_server_browser]
            )
        logging.info("Starting MCP server for files- 333")
        with trace("investigate"):
            logging.info("Starting MCP server for files- 444")
            await Runner.run(agent, "Find a great recipe for Banoffee Pie, then summarize it in markdown to banoffee.md")
            logging.info("Starting MCP server for files- 555")