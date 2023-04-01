#!/usr/bin/env python3

import datetime

import coin_prices
import impermanent_loss
import cakedefi_parser


def lambda_handler(event, context) -> None: # pylint: disable = unused-argument
    coinpairs = [(("bitcoin", "btc"), ("defichain", "dfi")), (("bitcoin-cash", "bch"), ("defichain", "dfi"))]
    for pair in coinpairs:
        main(pair, number_of_days_for_comparison = 30, currency = "eur")


# TODO: return comparison as json?!
# IMPORTANT: The tool displays some values with two decimals and truncates the rest. It does NOT round them in a mathematical sense!
# I.e. 0.6775 --> 0.677 instead of the expected 0.678
def main(coinpair_ids_symbols: tuple[tuple[str, str]], number_of_days_for_comparison: int, currency = "eur") -> None:
    # I don't know why pyright reports this error for the following line: "Index 1 is out of range for type tuple[tuple[str, str]] (reportGeneralTypeIssues)"
    coinpair_ids = [coinpair_ids_symbols[0][0], coinpair_ids_symbols[1][0]] # type: ignore
    current_coin_prices = coin_prices.get_current_coin_prices(coinpair_ids, currency = currency)
    datetime_utc = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days = number_of_days_for_comparison)
    historical_coin_prices = coin_prices.get_historical_coin_prices(coinpair_ids, datetime_utc, currency = currency)

    # I don't know why pyright reports this error for the following line: "Index 1 is out of range for type tuple[tuple[str, str]] (reportGeneralTypeIssues)"
    coinpair_symbols = (coinpair_ids_symbols[0][1], coinpair_ids_symbols[1][1]) # type: ignore
    print(f"Calculate impermanent loss for {coinpair_symbols} over the last {number_of_days_for_comparison} days...")
    _impermanent_loss = impermanent_loss.calculate_impermanent_loss(historical_coin_prices[coinpair_ids[0]][currency],
                                                                    historical_coin_prices[coinpair_ids[1]][currency],
                                                                    current_coin_prices[coinpair_ids[0]][currency],
                                                                    current_coin_prices[coinpair_ids[1]][currency])
    print(f">>>>>> Impermanent loss for {coinpair_symbols} over the last {number_of_days_for_comparison} days: {round(_impermanent_loss, 3)} %")


    apr = cakedefi_parser.get_apr_from_cakedefi(coinpair_symbols)
    print(f">>>>>> APR for Liquidity Pool {coinpair_symbols}: {round(apr, 3)} %")
    apr_per_days = apr/(365/number_of_days_for_comparison)
    print(f">>>>>> APR for Liquidity Pool {coinpair_symbols} per {number_of_days_for_comparison} days: {round(apr_per_days, 3)} %")

    print("\n=============================")
    print(f">>>>>> The Liquidity Mining yield for {coinpair_symbols} per {number_of_days_for_comparison} days is: {round(apr_per_days - _impermanent_loss, 3)} %\n")
    # TODO send mail via AWS SES


if __name__ == "__main__":
    lambda_handler({}, None) # pylint: disable = no-value-for-parameter
