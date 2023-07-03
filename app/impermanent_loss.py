from math import sqrt


# This function uses the Uniswap constant product formula to calculate the impermanent loss
def calculate_impermanent_losses(coin_pairs: list[dict], initial_prices: dict, current_prices: dict, currency: str) -> dict:
    print("Calculate impermanent losses for cryptocurrency pairs...")
    result = {}
    for pair in coin_pairs:
        print(f"Calculate il for {pair['symbols']}...")
        _impermanent_loss = _calculate_impermanent_loss(initial_prices[pair['coin_1']['id']][currency],
                                                        initial_prices[pair['coin_2']['id']][currency],
                                                        current_prices[pair['coin_1']['id']][currency],
                                                        current_prices[pair['coin_2']['id']][currency])
        _impermanent_loss = round(_impermanent_loss, 3)
        print(f"Impermanent loss for {pair['symbols']}: {_impermanent_loss} %")
        print("----------------------------")
        result[pair['symbols']] = _impermanent_loss
    return result


# This function uses the Uniswap constant product formula to calculate the impermanent loss
# To verify the result you can use this online calculator: https://dailydefi.org/tools/impermanent-loss-calculator/
def _calculate_impermanent_loss(coin1_initial_price: float, coin2_initial_price: float, coin1_current_price: float, coin2_current_price: float) -> float:
    print(f"Initial price coin 1: {coin1_initial_price}")
    print(f"Initial price coin 2: {coin2_initial_price}")
    print(f"Current price coin 1: {coin1_current_price}")
    print(f"Current price coin 2: {coin2_current_price}")

    # Explanation for calculation and formula: https://chainbulletin.com/impermanent-loss-explained-with-examples-math
    # The formula to calculate impermanent loss in percent is:
    # il_in_percent = (1 - stake_value/hold_value) * 100
    #
    # where:
    # stake_value = Q1_current * coin1_current_price + Q2_current * coin2_current_price
    #   with:
    #       Q1 and Q2 as the quantity of coin 1 and 2 in the liquidity pool
    #       Q1_pointintime = sqrt(k / r_pointintime)
    #       Q2_pointintime = sqrt(k * r_pointintime)
    #       k = Q1_pointintime * Q2_pointintime (constant product of quantities of coin 1 and 2)
    #       r = coin1_pointintime_price / coin2_pointintime_price
    #
    # hold_value = Q1_initial * coin1_current_price + Q2_initial * coin2_current_price
    #
    # We can eliminate the coin quantities in the formula as they are irrelevant for the impermanent loss and they are also reflected by the corresponding coin prices.
    # --> k = Q1_initial * Q2_initial = coin1_initial_price * coin2_initial_price
    # and we can also replace 'Q1_initial' with 'coin2_initial_price' resp. 'Q2_initial' with 'coin1_initial_price'.
    #
    # ==> According to that the formula for impermanent loss is:

    numerator = sqrt(coin1_initial_price * coin2_initial_price / (coin1_current_price / coin2_current_price)) * coin1_current_price + \
                sqrt(coin1_initial_price * coin2_initial_price * (coin1_current_price / coin2_current_price)) * coin2_current_price
    denominator = coin2_initial_price * coin1_current_price + coin1_initial_price * coin2_current_price
    il_in_percent = (1 - numerator/denominator) * 100

    return il_in_percent
