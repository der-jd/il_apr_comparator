#!/usr/bin/env python3


import datetime
import requests


# Coingecko API documentation: https://www.coingecko.com/en/api/documentation
API_BASE_URL = "https://api.coingecko.com/api/v3"


def get_coin_prices(coins: list[str], datetime_utc: datetime, currency: str = "eur") -> list[dict]:
    print(f"Get coin prices for {coins} in {currency}...")

    if not datetime_utc:
        return _get_current_coin_prices(coins, currency)
    else:
        prices = []
        for c in coins:
            data = _get_historical_coin_price(c, datetime_utc)
            prices.append({c: {currency: data['market_data']['current_price'][data['symbol']]}})
        return prices


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
def _get_current_coin_prices(coins: list[str], currency: str = "EUR") -> dict:
    url = f"{API_BASE_URL}/simple/price?ids={','.join(c for c in coins)}&vs_currencies={currency}"
    headers = {
        "accept": "application/json"
    }

    print(f"Call {url}...")
    response = requests.get(url, headers = headers, timeout = 10)

    if response.status_code != 200:
        raise RuntimeError(f"ERROR: API call failed!\n{response.status_code} {response.reason}")

    return response.json()


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
def _get_historical_coin_price(coin: str, datetime_utc: datetime) -> dict:
    date = datetime_utc.datetime.strftime("%d-%m-%Y")
    url = f"{API_BASE_URL}/coins/{coin}/history?date={date}"
    headers = {
        "accept": "application/json"
    }

    print(f"Call {url}...")
    response = requests.get(url, headers = headers, timeout = 10)

    if response.status_code != 200:
        raise RuntimeError(f"ERROR: API call failed!\n{response.status_code} {response.reason}")

    return response.json()
