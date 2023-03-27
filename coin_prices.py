#!/usr/bin/env python3


import datetime
import requests


# Coingecko API documentation: https://www.coingecko.com/en/api/documentation
API_BASE_URL = "https://api.coingecko.com/api/v3"


# coins: e.g. ["bitcoin", "ethereum", ...]
# Example for response body:
#{
#  "bitcoin": {
#    "eur": 25840
#  },
#  "ethereum": {
#    "eur": 1636.82
#  }
#}
def get_current_coin_prices(coins: list[str], currency: str = "eur") -> dict:
    print(f"Get current coin prices for {coins} in '{currency}'...")

    url = f"{API_BASE_URL}/simple/price?ids={','.join(c for c in coins)}&vs_currencies={currency}"
    headers = {
        "accept": "application/json"
    }

    print(f"Call {url}...")
    response = requests.get(url, headers = headers, timeout = 10)

    if response.status_code != 200:
        raise RuntimeError(f"ERROR: API call failed!\n{response.status_code} {response.reason}")

    return response.json()


# Example for return value:
#{
#  "bitcoin": {
#    "eur": 25840
#  },
#  "ethereum": {
#    "eur": 1636.82
#  }
#}
def get_historical_coin_prices(coins: list[str], datetime_utc: datetime.datetime, currency: str = "eur") -> dict:
    print(f"Get historical coin prices for {coins} in '{currency}'...")

    prices = {}
    for c in coins:
        data = _get_historical_coin_price(c, datetime_utc)
        prices[c] = {currency: data['market_data']['current_price'][currency]}
    return prices


# coin: e.g. "bitcoin" or "ethereum"
# Example for response body:
#{
#  "id": "ethereum",
#  "symbol": "eth",
#  "name": "Ethereum",
#  "localization": {
#    "en": "Ethereum",
#    "de": "Ethereum"
#  },
#  "image": {
#    "thumb": "https://assets.coingecko.com/coins/images/279/thumb/ethereum.png?1595348880",
#    "small": "https://assets.coingecko.com/coins/images/279/small/ethereum.png?1595348880"
#  },
#  "market_data": {
#    "current_price": {
#      "eur": 1127.1279368718483,
#      ...
#    },
#    "market_cap": {
#       ...
#    },
#    "total_volume": {
#       ...
#    }
#  },
#  "community_data": {
#       ...
#  },
#  "developer_data": {
#       ...
#    },
#    "commit_count_4_weeks": 29
#  },
#  "public_interest_stats": {
#    "alexa_rank": null,
#    "bing_matches": null
#  }
#}
def _get_historical_coin_price(coin: str, datetime_utc: datetime.datetime) -> dict:
    date = datetime_utc.strftime("%d-%m-%Y")
    print(f"Get coin prices at date {date}...")

    url = f"{API_BASE_URL}/coins/{coin}/history?date={date}"
    headers = {
        "accept": "application/json"
    }

    print(f"Call {url}...")
    response = requests.get(url, headers = headers, timeout = 10)

    if response.status_code != 200:
        raise RuntimeError(f"ERROR: API call failed!\n{response.status_code} {response.reason}")

    return response.json()
