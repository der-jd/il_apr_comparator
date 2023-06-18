import datetime
import requests


# Coingecko API documentation: https://www.coingecko.com/en/api/documentation
API_BASE_URL = "https://api.coingecko.com/api/v3"


def add_coin_info_for_symbols(coin_pairs: list[dict]) -> list[dict]:
    print("Add coin info for symbols...")
    for pair in coin_pairs:
        pair['coin_1'] = _find_matching_symbol(pair['coin_1'])
        pair['coin_2'] = _find_matching_symbol(pair['coin_2'])

    return coin_pairs


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
def get_current_coin_prices(coin_ids: set[str], currency: str = "eur") -> dict:
    print(f"Get current coin prices for {coin_ids} in '{currency}'...")

    url = f"{API_BASE_URL}/simple/price?ids={','.join(c for c in coin_ids)}&vs_currencies={currency}"
    headers = {
        "accept": "application/json"
    }

    print(f"Call {url}...")
    try:
        response = requests.get(url, headers = headers, timeout = 10)
        response.raise_for_status()
    except (requests.exceptions.RequestException, ValueError) as err:
        raise RuntimeError(f"ERROR: API call failed!\n{str(err)}") from err

    return response.json()


# coin ids: e.g. ["bitcoin", "ethereum", ...]
# Example for return value:
#{
#  "bitcoin": {
#    "eur": 25840
#  },
#  "ethereum": {
#    "eur": 1636.82
#  }
#}
def get_historical_coin_prices(coin_ids: set[str], datetime_utc: datetime.datetime, currency: str = "eur") -> dict:
    print(f"Get historical coin prices for {coin_ids} in '{currency}'...")

    prices = {}
    for c in coin_ids:
        data = _get_historical_coin_price(c, datetime_utc)
        prices[c] = {currency: data['market_data']['current_price'][currency]}
    return prices


# coin id: e.g. "bitcoin" or "ethereum"
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
def _get_historical_coin_price(coin_id: str, datetime_utc: datetime.datetime) -> dict:
    date = datetime_utc.strftime("%d-%m-%Y")
    print(f"Get coin prices for '{coin_id}' at date {date}...")

    url = f"{API_BASE_URL}/coins/{coin_id}/history?date={date}"
    headers = {
        "accept": "application/json"
    }

    print(f"Call {url}...")
    try:
        response = requests.get(url, headers = headers, timeout = 10)
        response.raise_for_status()
    except (requests.exceptions.RequestException, ValueError) as err:
        raise RuntimeError(f"ERROR: API call failed!\n{str(err)}") from err

    return response.json()


def _find_matching_symbol(coin: dict) -> dict:
    supported_coins = _get_supported_coins()
    symbol_found = False
    for supp_coin in supported_coins:
        if coin['symbol'].lower() == supp_coin['symbol'].lower():
            if coin['symbol'].lower() == "dfi": # special case for 'dfi' as there are multiple ids for this symbol
                if supp_coin['name'].lower() == "defichain":
                    coin['id'] = supp_coin['id']
                    coin['name'] = supp_coin['name']
                    symbol_found = True
                    break
            else:
                coin['id'] = supp_coin['id']
                coin['name'] = supp_coin['name']
                symbol_found = True
                break

    if not symbol_found:
        raise RuntimeError(f"ERROR: Cryptocurrency symbol '{coin['symbol']}' not supported or not found!")

    return coin


def _get_supported_coins(include_platform: bool = False) -> list[dict]:
    print("Get supported coins from Coingecko...")

    url = f"{API_BASE_URL}/coins/list?include_platform={include_platform}"
    headers = {
        "accept": "application/json"
    }
    print(f"Call {url}...")
    try:
        response = requests.get(url, headers = headers, timeout = 10)
        response.raise_for_status()
    except (requests.exceptions.RequestException, ValueError) as err:
        raise RuntimeError(f"ERROR: API call failed!\n{str(err)}") from err

    return response.json()
