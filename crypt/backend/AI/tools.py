# Imports
import os
import requests
import pandas as pd
from datetime import datetime

# Langchain
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool

"""
FUNCTIONS
"""

def get_all_coins():
    """
    Returns a response if a user asks for ALL coins.
    """
    
    return "Due to not being able to process the sheer number of coins I am unable to process this request. Please ask for a specific coin and I will find it."

def get_specific_coin_data(coin_data: str):
    """
    Returns specific cryptocurrency coin data from the coin gecko platform based on the provided coin name, symbol, or id.
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=1000"
    
    headers = {
        "accept": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("COIN_MARKET_CAP_TOKEN")
    }

    response = requests.get(url, headers=headers)
    coins = response.json().get("data", [])

    for coin in coins:
        if coin_data.lower() in [coin["name"].lower(), coin["symbol"].lower(), coin["slug"].lower()]:
            return coin

    return f"No data found for the provided coin: {coin_data}"

def get_specific_coin_price(coin_name: str):
    """
    Returns the USD price of a specific cryptocurrency coin from the CoinGecko platform based on the provided coin name, symbol, or id.
    """
    coin_data = get_specific_coin_data(coin_name)
    
    if isinstance(coin_data, str):
        # If the returned value is an error message, return it
        return coin_data
    
    # Extract the USD price from the coin data
    usd_price = coin_data.get('quote', {}).get('USD', {}).get('price')

    if usd_price is not None:
        return usd_price
    else:
        return f"USD price not found for the provided coin: {coin_name}"

def convert_coin_price(usd_coin_price: str, currency_to_convert_to: str):
    """
    Converts the given USD coin price to the specified currency using a conversion API.
    """
    # Get today's date in the format YYYY-MM-DD
    today_date = datetime.today().strftime('%Y-%m-%d')
    
    # Construct the URL for the API request
    url = f"https://api.fxratesapi.com/convert?from=USD&to={currency_to_convert_to}&date={today_date}&amount={usd_coin_price}&format=json"
    
    # Send a GET request to the conversion API
    response = requests.get(url)
    data = response.json()

    # Extract the converted amount from the response
    converted_amount = data.get('result')

    if converted_amount is not None:
        return converted_amount
    else:
        return f"Conversion result not found for the provided data: {usd_coin_price} to {currency_to_convert_to}"

def get_nft_data(nft_data: str):
    """
    Retrieves NFT data from the CoinGecko API based on the provided NFT data.

    Args:
        nft_data (str): The NFT data to retrieve data for.

    Returns:
        dict or str: The JSON response from the API if the request is successful, 
        otherwise a string indicating that no data was found for the provided NFT.
    """
    url = f"https://api.coingecko.com/api/v3/nfts/{nft_data.replace(' ', '-').lower()}"
    
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"No data found for the provided NFT: {nft_data}"

def get_derivative_data(derivative_data: str):
    """
    Returns a specific derivative and its respective data from the CoinGecko platform based on the provided information.
    """

    url = "https://api.coingecko.com/api/v3/derivatives/exchanges?order=name_asc&per_page=100"
    
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        exchanges = response.json()
        for exchange in exchanges:
            if derivative_data.lower() in [exchange["name"].lower(), exchange["id"].lower()]:
                return exchange
        return f"No data found for the provided derivative exchange: {derivative_data}"
    else:
        return f"Failed to fetch data from the API. Status code: {response.status_code}"


def get_trending_coins_nft_derivative():
    url = "https://api.coingecko.com/api/v3/search/trending"
    
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-zWJQ754BinqYbYC9po9Q7mXx"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        coins = data.get('coins', [])
        
        # Split the coins data into chunks
        chunk_size = 3  # Adjust the chunk size as needed
        chunks = [coins[i:i + chunk_size] for i in range(0, len(coins), chunk_size)]
        
        return chunks
    else:
        return f"Failed to fetch data from the API. Status code: {response.status_code}"



"""
CLASSES
"""
class CoinInput(BaseModel):
    coin_name: str = Field(description="Should be the ID# of a coin")

class MoneyInput(BaseModel):
    usd_coin_price: str = Field(description="Should be USD dollar value ($) of the coin")
    currency_to_convert_to: str = Field(description="This is the currency which the USD price is being converted TO")
    
class NFTInput(BaseModel):
    nft_data: str = Field(description="This is either the name, symbol or an id of a NFT collection as represented on the CoinGecko Website. ID all have hypens. For example: pudgy-penguins")
    
class DerivativeInput(BaseModel):
    derivative_data: str = Field(description="This is the name or an id of a derivative from a specific exchange")

"""
TOOL CREATION (combination of classes and functions)
"""

get_all_coins_tool = StructuredTool.from_function(
    func=get_all_coins,
    name="Get_ALL_Tokens",
    description="Returns an error message if the user asks for more coins than 10. For example: if the user asks for ALL tokens from a platform",
)

specific_coin_price_tool = StructuredTool.from_function(
    func=get_specific_coin_price,
    name="Specific_Tool_Data",
    description="Returns specific cryptocurrency coin data from the Coin Gecko platform. The JSON response from the Coin Gecko API containing information about the specified coin which should be used for data extraction.",
    args_schema=CoinInput   
)

convert_coin_price_tool = StructuredTool.from_function(
    func=convert_coin_price,
    name="Convert_Coin_Price",
    description="This converts the given USD coin price to the specified currency using a conversion API.",
    args_schema=MoneyInput
)

get_nft_data_tool = StructuredTool.from_function(
    func=get_nft_data,
    name="Get_NFT_Data",
    description="Returns ALL the NFT Data of a given NFT collection",
    args_schema=NFTInput
)

get_derivative_data_tool = StructuredTool.from_function(
    func=get_derivative_data,
    name="Get_Derviative_Data",
    description="Returns a specific derivative and its respective data from the CoinGecko platform based on the provided information.",
    args_schema=DerivativeInput
)

get_trending_coins_tool = StructuredTool.from_function(
    func=get_trending_coins_nft_derivative,
    name="Get_Trending_Coins_NFT_Derivative",
    description="Returns the trending search coins, nfts and categories on CoinGecko in the last 24 hours. Supports: Top 15 trending coins (sorted by the most popular user searches), Top 7 trending NFTs (sorted by the highest percentage change in floor prices), Top 5 trending categories (sorted by the most popular user searches)"
)

# ----------TESTING----------------
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from llm import LLM


tools = [get_all_coins_tool, specific_coin_price_tool, convert_coin_price_tool, get_nft_data_tool, get_derivative_data_tool, get_trending_coins_nft_derivative_tool]
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

agent = create_tool_calling_agent(LLM.gpt3_5, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(agent_executor.invoke({"input": "what is the trending coin's price today in JMD?"}))