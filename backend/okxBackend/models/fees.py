"""
    Returns the expected fee in USD for an order.
"""

def  calculate_fee(order_type='maker', fee_tier='tier_1', quantity_usd=10000):
    tier_fees = {
        "tier_1": {"maker": 0.00080, "taker": 0.00100},
        "tier_2": {"maker": 0.00075, "taker": 0.00090},
        "tier_3": {"maker": 0.00070, "taker": 0.00080},
        "tier_4": {"maker": 0.00065, "taker": 0.00070},
        "tier_5": {"maker": 0.00060, "taker": 0.00060},
    }

    fee_rate = tier_fees.get(fee_tier, tier_fees["tier_1"])
    role = "taker" if order_type == "market" else "maker"
    fee_pct = fee_rate[role]

    return round(quantity_usd * fee_pct, 6)