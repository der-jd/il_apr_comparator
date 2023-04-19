from math import sqrt


# TODO fix il calculation. check which formula is used. there are different il formulas in the internet # pylint: disable = fixme
def calculate_impermanent_loss(coin1_initial_price: float, coin2_initial_price: float, coin1_current_price: float, coin2_current_price: float) -> float:
    print(f"Initial price coin 1: {coin1_initial_price}")
    print(f"Initial price coin 2: {coin2_initial_price}")
    print(f"Current price coin 1: {coin1_current_price}")
    print(f"Current price coin 2: {coin2_current_price}")
    initial_lp = 2 * sqrt(coin1_initial_price * coin2_initial_price) / (coin1_initial_price + coin2_initial_price)
    current_lp = 2 * sqrt(coin1_current_price * coin2_current_price) / (coin1_current_price + coin2_current_price)
    return current_lp / initial_lp - 1
