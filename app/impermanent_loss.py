from math import sqrt


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


# TODO fix il calculation. check which formula is used. there are different il formulas in the internet # pylint: disable = fixme
def _calculate_impermanent_loss(coin1_initial_price: float, coin2_initial_price: float, coin1_current_price: float, coin2_current_price: float) -> float:
    print(f"Initial price coin 1: {coin1_initial_price}")
    print(f"Initial price coin 2: {coin2_initial_price}")
    print(f"Current price coin 1: {coin1_current_price}")
    print(f"Current price coin 2: {coin2_current_price}")
    initial_lp = 2 * sqrt(coin1_initial_price * coin2_initial_price) / (coin1_initial_price + coin2_initial_price)
    current_lp = 2 * sqrt(coin1_current_price * coin2_current_price) / (coin1_current_price + coin2_current_price)
    return current_lp / initial_lp - 1
