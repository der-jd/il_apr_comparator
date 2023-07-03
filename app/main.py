#!/usr/bin/env python3

import datetime
import json
import os

import aws
import coin_prices
import comparator
import impermanent_loss
import liquidity_mining_apr


# TODO trigger lambda automatically and regularly # pylint: disable = fixme
def lambda_handler(event, context) -> dict: # pylint: disable = unused-argument
    try:
        result = _main(number_of_days_for_comparison = 30, currency = "eur", scraping = "ai")
    except Exception: # pylint: disable = broad-exception-caught
        aws.send_sns_notification(topic_arn = aws.get_parameter_value(os.environ.get('SNS_TOPIC_ERRORS')), # pyright: ignore [reportGeneralTypeIssues]
                                  subject = "AWS Notification: ERROR IL-APR-Comparator",
                                  message = "The execution of the IL-APR-Comparator failed! Check the logs for further info.")
        raise

    aws.send_sns_notification(topic_arn = aws.get_parameter_value(os.environ.get('SNS_TOPIC_RESULT')), # pyright: ignore [reportGeneralTypeIssues],
                              subject = "AWS Notification: IL-APR-Comparator",
                              message = json.dumps(result, indent = 4))
    return result


# IMPORTANT: The tool displays some values with two decimals and truncates the rest. It does NOT round them in a mathematical sense!
# I.e. 0.6775 --> 0.677 instead of the expected 0.678
def _main(number_of_days_for_comparison: int, currency = "eur", scraping = "classic") -> dict:
    # Get APRs for Liquidity mining
    coin_pairs = liquidity_mining_apr.get_apr(scraping = scraping)

    # Get coin prices
    coin_pairs = coin_prices.add_coin_info_for_symbols(coin_pairs)
    coin_ids = _get_coin_ids(coin_pairs)
    current_coin_prices = coin_prices.get_current_coin_prices(coin_ids, currency = currency)
    datetime_utc = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days = number_of_days_for_comparison)
    historical_coin_prices = coin_prices.get_historical_coin_prices(coin_ids, datetime_utc, currency = currency)

    # Calculate impermanent losses
    impermanent_losses = impermanent_loss.calculate_impermanent_losses(coin_pairs, historical_coin_prices, current_coin_prices, currency)

    # Compare impermanent loss to APR
    return comparator.compare_apr_to_il(coin_pairs, impermanent_losses, number_of_days_for_comparison)


def _get_coin_ids(coin_pairs: list[dict]) -> set[str]:
    result = set()
    for pair in coin_pairs:
        result.add(pair['coin_1']['id'])
        result.add(pair['coin_2']['id'])
    return result


if __name__ == "__main__":
    _main(number_of_days_for_comparison = 30, currency = "eur", scraping = "classic")
