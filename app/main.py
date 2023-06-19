#!/usr/bin/env python3

import datetime

import cakedefi_parser
import coin_prices
import impermanent_loss


def lambda_handler(event, context) -> None: # pylint: disable = unused-argument
    _main(number_of_days_for_comparison = 30, currency = "eur")


# TODO: return comparison as json?! # pylint: disable = fixme
# IMPORTANT: The tool displays some values with two decimals and truncates the rest. It does NOT round them in a mathematical sense!
# I.e. 0.6775 --> 0.677 instead of the expected 0.678
def _main(number_of_days_for_comparison: int, currency = "eur") -> None:
    # Get APRs from Cake Defi
    coin_pairs = cakedefi_parser.get_aprs_from_cakedefi()

    # Get coin prices
    coin_pairs = coin_prices.add_coin_info_for_symbols(coin_pairs)
    coin_ids = _get_coin_ids(coin_pairs)
    current_coin_prices = coin_prices.get_current_coin_prices(coin_ids, currency = currency)
    datetime_utc = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days = number_of_days_for_comparison)
    historical_coin_prices = coin_prices.get_historical_coin_prices(coin_ids, datetime_utc, currency = currency)

    # Calculate impermanent loss
    for pair in coin_pairs:
        print(f"Calculate impermanent loss for {pair['symbols']} over the last {number_of_days_for_comparison} days...")
        _impermanent_loss = impermanent_loss.calculate_impermanent_loss(historical_coin_prices[pair['coin_1']['id']][currency],
                                                                        historical_coin_prices[pair['coin_2']['id']][currency],
                                                                        current_coin_prices[pair['coin_1']['id']][currency],
                                                                        current_coin_prices[pair['coin_2']['id']][currency])
        print(f">>>>>> Impermanent loss for {pair['symbols']} over the last {number_of_days_for_comparison} days: {round(_impermanent_loss, 3)} %")


        print(f">>>>>> APR for Liquidity Pool {pair['symbols']}: {round(float(pair['apr']), 3)} %")
        apr_per_days = float(pair['apr'])/(365/number_of_days_for_comparison)
        print(f">>>>>> APR for Liquidity Pool {pair['symbols']} per {number_of_days_for_comparison} days: {round(apr_per_days, 3)} %")

        print("\n=============================")
        print(f">>>>>> The Liquidity Mining yield for {pair['symbols']} per {number_of_days_for_comparison} days is: {round(apr_per_days - _impermanent_loss, 3)} %\n")
        # TODO send mail via AWS SES # pylint: disable = fixme


def _get_coin_ids(coin_pairs: list[dict]) -> set[str]:
    result = set()
    for pair in coin_pairs:
        result.add(pair['coin_1']['id'])
        result.add(pair['coin_2']['id'])
    return result


if __name__ == "__main__":
    lambda_handler({}, None) # pylint: disable = no-value-for-parameter
