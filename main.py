#!/usr/bin/env python3

import datetime

import coin_prices
import impermanent_loss
import cakedefi_parser


if __name__ == "__main__":
    coins = ["bitcoin", "bitcoin-cash", "defichain"]
    days_for_il = 30
    currency = "eur"
    current_coin_prices = coin_prices.get_current_coin_prices(coins, currency = currency)
    datetime_utc = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days = days_for_il)
    historical_coin_prices = coin_prices.get_historical_coin_prices(coins, datetime_utc, currency = currency)

    print(f"Calculate impermanent loss for BTC-DFI over the last {days_for_il} days...")
    il_btc_dfi = impermanent_loss.calculate_impermanent_loss(historical_coin_prices["bitcoin"][currency],
                                                                historical_coin_prices["defichain"][currency],
                                                                current_coin_prices["bitcoin"][currency],
                                                                current_coin_prices["defichain"][currency])
    print(f"Impermanent loss for BTC-DFI over the last {days_for_il} days: {il_btc_dfi}")

    print(f"Calculate impermanent loss for BCH-DFI over the last {days_for_il} days...")
    il_bch_dfi = impermanent_loss.calculate_impermanent_loss(historical_coin_prices["bitcoin-cash"][currency],
                                                                historical_coin_prices["defichain"][currency],
                                                                current_coin_prices["bitcoin-cash"][currency],
                                                                current_coin_prices["defichain"][currency])
    print(f"Impermanent loss for BCH-DFI over the last {days_for_il} days: {il_bch_dfi}")

    apr_btc_dfi = cakedefi_parser.get_apr_from_cakedefi(("BTC", "DFI"))
    print(f">>>>>> APR for Liquidity Pool BTC-DFI: {apr_btc_dfi}")
    apr_bch_dfi = cakedefi_parser.get_apr_from_cakedefi(("BCH", "DFI"))
    print(f">>>>>> APR for Liquidity Pool BCH-DFI: {apr_bch_dfi}")

    # TODO send mail via AWS SNS
