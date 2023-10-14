import os

import aws
import classic_scraping
import ai_scraping


# Example for returned list:
# [
#   {
#     "symbols": "BTC-DFI",
#     "coin_1": {
#       "id": "bitcoin",
#       "symbol": "btc",
#       "name": "Bitcoin"
#     },
#     "coin_2": {
#       "id": "defichain",
#       "symbol": "dfi",
#       "name": "DeFiChain"
#     },
#     "apr": "10"
#   },
#   {
#     "symbols": "ETH-DFI",
#     "coin_1": {
#       "id": "ethereum",
#       "symbol": "eth",
#       "name": "Ethereum"
#     },
#     "coin_2": {
#       "id": "defichain",
#       "symbol": "dfi",
#       "name": "DeFiChain"
#     },
#     "apr": "8"
#   }
# ]
def get_apr(scraping: str) -> list[dict]:
    print("Get APR for Liquidity Mining from Bake website...")

    if scraping == "classic":
        print("Use classic scraping to extract data...")
        return classic_scraping.get_apr()

    if scraping == "ai":
        print("Use artificial intelligence based scraping to extract data...")
        return ai_scraping.get_apr()

    raise RuntimeError(f"ERROR: Scraping method '{scraping}' unknown!")

def keep_only_specified_coin_pairs(all_coin_pairs: list[dict]):
    print("Impermanent loss will only be calculated for the specified coin pairs:")
    specified_coin_pairs = list(aws.get_parameter_value(os.environ.get('BAKE_COIN_PAIRS_FOR_IL')).split(",")) # pyright: ignore [reportGeneralTypeIssues]
    if not specified_coin_pairs:
        raise ValueError("ERROR: No coin pairs specified! Please enter a list of pairs in the according Parameter Store entry.")
    print(specified_coin_pairs)

    print("Discard other coin pairs from the list...")
    resulting_list = []
    for p in all_coin_pairs:
        if p['symbols'] in specified_coin_pairs:
            resulting_list.append(p)

    if not resulting_list:
        raise RuntimeError("ERROR: Resulting list is empty! None of the specified coin pairs matched with the ones extracted from Bake.")
    print(f"Resulting list:\n{resulting_list}")

    return resulting_list
