# Imports
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Langchain
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool
from langchain_experimental.utilities import PythonREPL
from llm import LLM

# Phidata
from phi.assistant.python import PythonAssistant
from phi.llm.openai import OpenAIChat

# Loading the environmental variables from the containing folder
load_dotenv()

"""
FUNCTIONS
"""

def fetch_data(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

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
    coins = fetch_data(url, headers).get("data", [])

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
    response = fetch_data(url, headers)
    
    if response:
        return response
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
    response = fetch_data(url, headers)
    
    if response:
        exchanges = response
        for exchange in exchanges:
            if derivative_data.lower() in [exchange["name"].lower(), exchange["id"].lower()]:
                return exchange
        return f"No data found for the provided derivative exchange: {derivative_data}"
    else:
        return f"Failed to fetch data from the API."

def get_trending_coins():
    """
    Fetches and processes trending coins data from the CoinGecko API, removing 'price_change_percentage_24h' from each coin's data.

    Returns:
        list: A list of dictionaries, each representing a trending coin with its data, excluding 'price_change_percentage_24h'.
    """
    url = "https://api.coingecko.com/api/v3/search/trending"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
    }
    data = fetch_data(url, headers)
    coins_data = data.get('coins', [])

    for coin in coins_data:
        # Remove 'price_change_percentage_24h' from the coin data
        if 'price_change_percentage_24h' in coin.get('item', {}).get('data', {}):
            del coin['item']['data']['price_change_percentage_24h']

    return coins_data

def get_trending_nfts():
    """
    Fetches and returns trending NFTs data from the CoinGecko API.

    This function sends a GET request to the CoinGecko API to retrieve trending NFTs data. It sets the 'accept' header to 'application/json' to specify the expected response format and includes the API key in the 'x-cg-demo-api-key' header for authentication. The function then parses the response and returns a list of trending NFTs data. If no NFTs data is found, an empty list is returned.

    Returns:
        list: A list of dictionaries, each representing a trending NFT with its data.
    """
    url = "https://api.coingecko.com/api/v3/search/trending"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
    }
    data = fetch_data(url, headers)
    return data.get('nfts', [])

def get_trending_categories():
    """
    Fetches and returns trending categories data from the CoinGecko API.

    This function sends a GET request to the CoinGecko API to retrieve trending categories data. It sets the 'accept' header to 'application/json' to specify the expected response format and includes the API key in the 'x-cg-demo-api-key' header for authentication. The function then parses the response and returns a list of trending categories data. If no categories data is found, an empty list is returned.

    Returns:
        list: A list of dictionaries, each representing a trending category with its data.
    """
    url = "https://api.coingecko.com/api/v3/search/trending"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
    }
    data = fetch_data(url, headers)
    return data.get('categories', [])

def get_historical_chart_data_by_id(coin_name: str, days: int, chart_data_type: str):
    """
    Gets the historical chart data of a coin including time in UNIX, price, market cap and 24hrs volume based on particular coin id from the CoinGecko API.

    Args:
        coin_name (str): The ID of the cryptocurrency coin for which to fetch historical data.
        days (int): The number of days for which to fetch historical data.

    Returns:
        dict: A dictionary containing the historical data for the specified coin over the specified number of days. If no data is found, an empty dictionary is returned.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_name}/market_chart?vs_currency=usd&days={days}&interval=daily&precision=full"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
    }
    response_data = fetch_data(url, headers)
    
    # Extract the requested data
    if chart_data_type in response_data:
        return {chart_data_type: response_data[chart_data_type]}
    else:
        return {"error": f"Data type '{chart_data_type}' not found in the response."}

def get_historical_chart_data_by_id_timerange(coin_name: str, from_: int, to_: str):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_name}/market_chart/range?vs_currency=usd&from={from_}&to={to_}&precision=full"


    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
    }
    data = fetch_data(url, headers)
    return data

def get_ohlc_chat_by_id(coin_name: str, days: int):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_name}/ohlc?vs_currency=usd&days={days}&precision=full"
    
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
    }
    
    data = fetch_data(url, headers)
    
    return data


"""
CLASSES
"""

# CoinInput class is used to define the input structure for coin-related operations.
# It contains a single field 'coin_name' which should be the ID# of a coin.
class CoinInput(BaseModel):
    coin_name: str = Field(description="Should be the ID# of a coin")

# MoneyInput class is used to define the input structure for currency conversion operations.
# It contains two fields: 'usd_coin_price' for the USD dollar value ($) of the coin and 'currency_to_convert_to' for the target currency.
class MoneyInput(BaseModel):
    usd_coin_price: str = Field(description="Should be USD dollar value ($) of the coin")
    currency_to_convert_to: str = Field(description="This is the currency which the USD price is being converted TO")

# NFTInput class is used to define the input structure for NFT-related operations.
# It contains a single field 'nft_data' which can be the name, symbol, or an id of a NFT collection as represented on the CoinGecko Website.
# IDs of NFT collections on CoinGecko typically have hyphens. For example: pudgy-penguins.
class NFTInput(BaseModel):
    nft_data: str = Field(description="This is either the name, symbol or an id of a NFT collection as represented on the CoinGecko Website. ID all have hypens. For example: pudgy-penguins")

# DerivativeInput class is used to define the input structure for derivative-related operations.
# It contains a single field 'derivative_data' which can be the name or an id of a derivative from a specific exchange.
class DerivativeInput(BaseModel):
    derivative_data: str = Field(description="This is the name or an id of a derivative from a specific exchange")

class HistoricalData(BaseModel):
    coin_name: str = Field(description="The ID # of a coin")
    days: int = Field(description="Number of days for historical data")
    chart_data_type: str = Field(description="What type of data is being asked for. Can ONLY be 3 options: prices, market_caps, volume (total). If the option given sounds close please change it to one of the 3 options. Example: the user gives 'price' it should be converted to prices ")

class OHLCData(BaseModel):
    coin_name: str = Field(description="The ID # of a coin")
    days: int = Field(description="Number of days for historical data")

class HistoricalTimeRangeData(BaseModel):
    coin_name: str = Field(description="The ID # of a coin")
    from_: str = Field(description="The date from which to start the historical data. Should be converted from natural language to UNIX timestamp")
    to_: str = Field(description="The date which historical data should end at. Should be converted from natural language to UNIX timestamp")

class AIPrompt(BaseModel):
    message: str = Field(description="The text prompt for the AI to process")

"""
TOOL CREATION (combination of classes and functions)
"""

# This tool returns an error message if the user asks for more coins than 10.
get_all_coins_tool = StructuredTool.from_function(
    func=get_all_coins,
    name="Get_ALL_Tokens",
    description="Returns an error message if the user asks for more coins than 10. For example: if the user asks for ALL tokens from a platform",
)

# This tool returns specific cryptocurrency coin data from the Coin Gecko platform.
specific_coin_price_tool = StructuredTool.from_function(
    func=get_specific_coin_price,
    name="Specific_Tool_Data",
    description="Returns specific cryptocurrency coin data from the Coin Gecko platform. The JSON response from the Coin Gecko API containing information about the specified coin which should be used for data extraction.",
    args_schema=CoinInput   
)

# This tool converts the given USD coin price to the specified currency using a conversion API.
convert_coin_price_tool = StructuredTool.from_function(
    func=convert_coin_price,
    name="Convert_Coin_Price",
    description="This converts the given USD coin price to the specified currency using a conversion API.",
    args_schema=MoneyInput
)

# This tool returns ALL the NFT Data of a given NFT collection.
get_nft_data_tool = StructuredTool.from_function(
    func=get_nft_data,
    name="Get_NFT_Data",
    description="Returns ALL the NFT Data of a given NFT collection",
    args_schema=NFTInput
)

# This tool returns a specific derivative and its respective data from the CoinGecko platform based on the provided information.
get_derivative_data_tool = StructuredTool.from_function(
    func=get_derivative_data,
    name="Get_Derviative_Data",
    description="Returns a specific derivative and its respective data from the CoinGecko platform based on the provided information.",
    args_schema=DerivativeInput
)

# This tool returns the trending coins data from the CoinGecko platform.
get_trending_coins_tool = StructuredTool.from_function(
    func=get_trending_coins,
    name="Get_Trending_Coins",
    description="Returns the trending coins data from the CoinGecko platform.",
    args_schema=None
)

# This tool returns the trending NFTs data from the CoinGecko platform.
get_trending_nfts_tool = StructuredTool.from_function(
    func=get_trending_nfts,
    name="Get_Trending_NFTs",
    description="Returns the trending NFTs data from the CoinGecko platform.",
    args_schema=None
)

# This tool returns the trending categories data from the CoinGecko platform.
get_trending_categories_tool = StructuredTool.from_function(
    func=get_trending_categories,
    name="Get_Trending_Categories",
    description="Returns the trending categories data from the CoinGecko platform.",
    args_schema=None
)

# Python Tool
python_assistant = PythonAssistant(
    llm=OpenAIChat(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_TOKEN")),
    pip_install=True,
    show_function_calls=True,
    run_code=True
)

python_assistant_tool = StructuredTool.from_function(
    func=python_assistant.print_response,
    description="A Python shell for data analysis, predictions, converting natural language dates to UNIX timestamps and machine learning. Use this to execute python commands. Input should be a valid python command.",
    name="python_assistant",
    args_schema=AIPrompt
)

# Get Historical Dat By ID Tool
get_historical_data_by_id_tool = StructuredTool.from_function(
    func=get_historical_chart_data_by_id,
    name="Get_Historical_Data_By_ID",
    description="Returns historical data for a given cryptocurrency by its ID.",
    args_schema=HistoricalData
)

get_historical_data_within_timeRange_by_id_tool = StructuredTool.from_function(
    func=get_historical_chart_data_by_id_timerange,
    name="Get_Historical_Data_By_ID_TimeRange",
    description="Returns historical data for a given cryptocurrency by its ID within a specified UNIX timestamped time range.",
    args_schema=HistoricalTimeRangeData
)

ohlc_tool = StructuredTool.from_function(
    func=get_ohlc_chat_by_id,
    name="OHLC_Tool",
    description="Returns the Open, High, Low, Close data for a given cryptocurrency over a specified number of days.",
    args_schema=OHLCData
)


# ----------TESTING----------------
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from llm import LLM


tools = [get_all_coins_tool, specific_coin_price_tool, convert_coin_price_tool, get_nft_data_tool, get_derivative_data_tool, get_trending_coins_tool, get_trending_nfts_tool, get_trending_categories_tool, get_historical_data_by_id_tool, ohlc_tool, python_assistant_tool]

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

print(agent_executor.invoke(
    {
        "input": "Using ALL of the last 30 days of prices for Bitcoin predict what the prices will be 7 days from now. Do not show any plots. ONLY print the 7 days values by their date."
    })
    )