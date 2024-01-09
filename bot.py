import discord

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Enable message content intent
from dotenv import load_dotenv
import os
load_dotenv()


coinapi_key = os.getenv('COINMARKETAPIKEY')
discordapi = os.getenv('DISCORDKEY')


import requests
yourapikey = '13783b1c-87b6-4394-8ef1-b6a96e75077e'
def get_trending_coins(api_key):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/most-visited"
    parameters = {
        'start': '1',
        'limit': '10',
        'time_period': '24h'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    # print(f"API Response: {response.text}")  # Print the raw API response

    response = requests.get(url, headers=headers, params=parameters)
    print(f"API Response: {response.text}")  # Print the raw API response

    data = response.json()
    return data


def get_categories(api_key, start=1, limit=22):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/categories"
    parameters = {
        'start': start,
        'limit': limit
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    # print(f"API Response: {response.text}")  # Print the raw API response
    response = requests.get(url, headers=headers, params=parameters)
    print(f"API Response: {response.text}")  # Print the raw API response

    data = response.json()
    return data



def get_category_details(api_key, category_id, start=1, limit=10):
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/category"
    parameters = {
        'id': category_id,
        'start': start,
        'limit': limit
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }
    # print(f"API Response: {response.text}")  # Print the raw API response

    response = requests.get(url, headers=headers, params=parameters)
    print(f"API Response: {response.text}")  # Print the raw API response

    data = response.json()
    return data


mydict = {
    1: "659392fd54b2742440bf0dde",
    2: "658e1127598b0275bafcb61c",
    3: "658c3f5c517c467a48f469f6",
    4: "658b5d8f517c467a48f445cd",
    5: "65817d327289e144e00613fe",
    6: "65817cf07289e144e00613ea",
    7: "655c563a19d020516fba113a",
    8: "655c542219d020516fba1022",
    9: "655b7f01b5b0d755998089bd",
    10: "654a0c87ba37f269c8016129",
    11: "6513a01333cae40c55d561e0",
    12: "64e47d21ae41d47d40cc07bc",
    13: "64db35dd28bd4735cb57c3a9",
    14: "64dadf1428bd4735cb57b43a",
    15: "64ca337fcad87e003b862a43",
    16: "64c7867acad87e003b856825",
    17: "64bfbf3a1e8d1f05fac5ad33",
    18: "64bbb61c65d6d5788642471d",
    19: "64bb8c5065d6d57886423e56",
    20: "64b50425e94fbc1954ae51cc",
    21: "64b01bff8610a065fa40bc56",
    22: "64928c41e3f98f1180d39e9c"
}





client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    print(f'Message received: {message.content}') # Add this line
    if message.author == client.user:
        print(f'jattt')
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('tell me a fact'):
        await message.channel.send('Tenvols gets no bitches')
    if message.content.startswith('tell me a lie'):
        await message.channel.send('Tenvols gets bitches')
    if message.content.startswith('bummer'):
        await message.channel.send('bummer Indeed')
    if message.content.startswith('!trendingcoins'):
        try:
            api_key = coinapi_key  # Replace with your CoinMarketCap API key
            trending_data = get_trending_coins(api_key)
            if 'data' in trending_data:
                reply_message = "Trending Coins:\n"
                for coin in trending_data['data']:
                    reply_message += f"{coin['name']} (Symbol: {coin['symbol']}) - Price: ${coin['quote']['USD']['price']:.2f}\n"
                await message.channel.send(reply_message)
            else:
                await message.channel.send("Error fetching data.")
        except Exception as e:
            print(f"Error: {e}")  # Print the exception
            await message.channel.send(f"An error occurred: {e}")
    if message.content.startswith('!viewcategories'):
        try:
            api_key = coinapi_key  # Replace with your CoinMarketCap API key
            categories_data = get_categories(api_key)
            if 'data' in categories_data:
                reply_message = "Coin Categories:\n"
                i=1
                for category in categories_data['data']:
                    reply_message += f"{i} {category['name']}: Market Cap ${category['market_cap']:.2f}, Avg Price Change {category['avg_price_change']:.2%}\n"
                    i = i+1
                await message.channel.send(reply_message)
            else:
                await message.channel.send("Error fetching category data.")
        except Exception as e:
            await message.channel.send(f"An error occurred: {e}")
    
    if message.content.startswith('!viewcategory '):
        try:
            category_id = message.content.split(' ')[1]  # Get the Category ID from the message
            api_key =coinapi_key  # Replace with your CoinMarketCap API key
            realid = mydict[int(category_id)]
            category_data = get_category_details(api_key, realid)
            if 'data' in category_data:
                category = category_data['data']
                reply_message = f"Category: {category['name']}\n"
                reply_message += f"Market Cap: ${category['market_cap']:.2f}, Avg Price Change: {category['avg_price_change']:.2%}\n"
                reply_message += "Coins:\n"
                for coin in category['coins']:
                    quote = coin['quote']['USD']

                    reply_message += f"{coin['name']} (Symbol: {coin['symbol']}):\n" \
                                 f"- Price: ${quote['price']:.2f}\n" \
                                 f"- Avg Price Change: {quote.get('percent_change_24h', 'N/A'):.2%}\n" \
                                 f"- Market Cap: ${quote['market_cap']:.2f}\n" \
                                 f"- Volume: ${quote['volume_24h']:.2f}\n" \
                                 f"- Market Cap Change: {quote.get('percent_change_24h', 'N/A'):.2%}\n\n"
                await message.channel.send(reply_message)
            else:
                await message.channel.send("Error fetching category data.")
        except Exception as e:
            print(f"Error: {e}")  # Print the exception

            await message.channel.send(f"An error occurred: {e}")
    # if message.content.startswith('!viewcategories'):
    #     try:
    #         api_key = '13783b1c-87b6-4394-8ef1-b6a96e75077e'  # Replace with your CoinMarketCap API key
    #         categories_data = get_categories(api_key)
    #         if 'data' in categories_data:
    #             reply_message = "Coin Categories:\n"
    #             for category in categories_data['data']:
    #                 reply_message += f"ID: {category['id']} - {category['name']}\n"
    #             await message.channel.send(reply_message)
    #         else:
    #             await message.channel.send("Error fetching category data.")
    #     except Exception as e:
    #         await message.channel.send(f"An error occurred: {e}")



client.run(discordapi)