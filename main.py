#!/usr/bin/env python3

import datetime

import coin_prices
import impermanent_loss
import cakedefi_parser


def main(coinpair_ids_symbols: tuple[tuple], number_of_days_for_comparison: int, currency = "eur") -> None:
    coinpair_ids = [coinpair_ids_symbols[0][0], coinpair_ids_symbols[1][0]]
    current_coin_prices = coin_prices.get_current_coin_prices(coinpair_ids, currency = currency)
    datetime_utc = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days = number_of_days_for_comparison)
    historical_coin_prices = coin_prices.get_historical_coin_prices(coinpair_ids, datetime_utc, currency = currency)

    coinpair_symbols = (coinpair_ids_symbols[0][1], coinpair_ids_symbols[1][1])
    print(f"Calculate impermanent loss for {coinpair_symbols} over the last {number_of_days_for_comparison} days...")
    il = impermanent_loss.calculate_impermanent_loss(historical_coin_prices[coinpair_ids[0]][currency],
                                                        historical_coin_prices[coinpair_ids[1]][currency],
                                                        current_coin_prices[coinpair_ids[0]][currency],
                                                        current_coin_prices[coinpair_ids[1]][currency])
    print(f"Impermanent loss for {coinpair_symbols} over the last {number_of_days_for_comparison} days: {il}")

    apr = cakedefi_parser.get_apr_from_cakedefi(coinpair_symbols)
    print(f">>>>>> APR for Liquidity Pool {coinpair_symbols}: {apr}")

    # TODO send mail via AWS SNS


if __name__ == "__main__":
    # Input
    coinpair_ids_symbols = (("bitcoin", "btc"), ("defichain", "dfi"))
    main(coinpair_ids_symbols, number_of_days_for_comparison = 30, currency = "eur")
    coinpair_ids_symbols = (("bitcoin-cash", "bch"), ("defichain", "dfi"))
    main(coinpair_ids_symbols, number_of_days_for_comparison = 30, currency = "eur")
