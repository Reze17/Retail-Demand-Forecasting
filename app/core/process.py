import asyncio
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient  
from langgraph.checkpoint.memory import InMemorySaver
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
import os

from app.core.prompt import SYSTEM_PROMPT

load_dotenv()

checkpointer = InMemorySaver()

config = {
    "configurable": {
        "thread_id": "1"  
    }
}

async def chat_agent():
    llm = ChatGroq(
        model="qwen/qwen3-32b",
        temperature=0,
        max_tokens=None,
        reasoning_format="parsed",
        timeout=None,
        max_retries=2,
    )
    McpConfig = {
    
     "mysql": {
      "command": "python",
      "transport":"stdio",
      "args": [
        "C:\\Users\\rjosepharon\\OneDrive - Stony Brook University\\Documents\\retail project\\data cleaning\\retailfastapi\\mysql_mcp_server\\src\\mysql_mcp_server\\server.py"
      ],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3307",
        "MYSQL_USER": "root",
        "MYSQL_PASSWORD": "12345r",
        "MYSQL_DATABASE": "grocery_inventory_db"
      }
    }
  

}
    

    client = MultiServerMCPClient(McpConfig)
    tools = await client.get_tools()

    agent = create_agent(
        llm,
        tools=tools,
        system_prompt= SYSTEM_PROMPT,
        checkpointer=checkpointer
    )

    return agent


async def main():
    agent = await chat_agent()

    response = await agent.ainvoke({
        "messages": [
            {"role": "user", "content": "What are the tools you have"}
        ]
    }, config)

    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())