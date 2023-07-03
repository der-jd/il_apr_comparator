# il-apr-comparator

[![CircleCI](https://circleci.com/gh/der-jd/il_apr_comparator.svg?style=shield&circle-token=8d10a608bd794e76c975b0bdedae7e1600c81cdc)](https://circleci.com/gh/der-jd/il_apr_comparator)

This tool takes a pair of cryptocurrencies for a Liquidity Mining Pool on `Bake` (https://app.bake.io/liquidity-mining). It calculates for a given period of time the Impermanent Loss (IL) of the pool. Then it compares the IL to the Annual Percentage Rate (APR) of the liquidity pool and sends a notification to subscribers informing about the difference between IL and APR.

## Update dependencies

- Install `pipreqs` Python package:
  - `pip install pipreqs`
- Create `requirements.txt`. Use `--force` to override already existent file:
  - `pipreqs --force <path_to_source_folder>`
- Manually (re)add any necessary dependencies removed by `pipreqs` (e.g. `lxml`)
