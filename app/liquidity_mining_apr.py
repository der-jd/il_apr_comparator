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
