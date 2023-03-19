#!/usr/bin/env python3


import datetime
import requests

import boto3


API_BASE_URL = "https://pro-api.coinmarketcap.com"
AWS_SSM_NAME_API_KEY = "coinmarketcap-api-key"


def get_coin_prices(coins: list[str], date: datetime, currency: str = "EUR") -> dict:
    if not date:
        url = f"{API_BASE_URL}/v2/cryptocurrency/quotes/latest?symbol={','.join(c for c in coins)}&convert={currency}"
    else:
        url = f"{API_BASE_URL}/v1/cryptocurrency/quotes/historical?symbol={','.join(c for c in coins)}&convert={currency}" # TODO: not available for Basis plan --> need another API

    headers = {
        "Accept": "application/json",
        "X-CMC_PRO_API_KEY": _get_api_key()
    }
    response = requests.get(url, headers = headers, timeout = 10)

    if response.status_code != 200:
        raise RuntimeError(f"ERROR: API call failed!\n{response.status_code} {response.reason}")

    return response.json()


def _get_api_key() -> str:
    ssm_client = boto3.client('ssm')
    return ssm_client.get_parameter(Name = AWS_SSM_NAME_API_KEY)
