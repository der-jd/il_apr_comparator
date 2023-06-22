import pprint

def compare_apr_to_il(coin_pairs: list[dict], impermanent_losses: dict, number_of_days_for_comparison: int) -> dict:
    print("Compare APR to impermanent loss for the given cryptocurrency pairs...")
    result = {}
    for pair in coin_pairs:
        apr = round(float(pair['apr']), 3)
        apr_per_days = round(float(pair['apr'])/(365/number_of_days_for_comparison), 3)
        result[pair['symbols']] = {
            "apr": apr,
            "number_of_days": number_of_days_for_comparison,
            "apr_per_days": apr_per_days,
            "impermanent_loss": impermanent_losses[pair['symbols']],
            "yield": round(apr_per_days - impermanent_losses[pair['symbols']], 3)
        }

    print("\n\n=============================")
    print(f">>>>>> Comparison between the APRs of the Liquidity Mining pools of 'Bake' and the impermanent losses over the last {number_of_days_for_comparison} days:\n")
    pprint.pprint(result)
    return result
