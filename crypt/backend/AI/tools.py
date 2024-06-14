# Imports
import os
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
import requests


#class CoinInput(BaseModel):
#    coin_name: str = Field(description="Should be the name of a coin")

#@tool("Coins List (ID Map)", args_schema=CoinInput, return_direct=True)
def get_all_coins(coin_name: str):
    """
    Returns a list of all cryptocurrency coins from the coin gecko platform.
    """
    url = "https://api.coingecko.com/api/v3/coins/list"
    
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
    }

    response = requests.get(url, headers=headers)

    return response.text


# ----------TESTING----------------
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from llm import LLM


tools = [get_all_coins]
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful crypto assistant with access to a wide range of tools to help answer questions about cryptocurrencies.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

#agent = create_tool_calling_agent(LLM.gpt3_5, tools, prompt)
#
#agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
#print(agent_executor.invoke({"input": "What is the name of the first coin on the platform?"}))

print(get_all_coins(""))