# il-apr-comparator

This tool takes a pair of cryptocurrencies for a Liquidity Mining Pool on `CakeDefi`. It calculates for a given period of time the Impermanent Loss (IL) of the pool. Then it compares the IL to the Annual Percentage Rate (APR) of the liquidity pool and sends a notification to subscribers informing about the difference between IL and APR.

## Update dependencies

- Install `pipreqs` Python package:
  - `pip install pipreqs`
- Create `requirements.txt`. Use `--force` to override already existent file:
  - `pipreqs --force <path_to_source_folder>`

