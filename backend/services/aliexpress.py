"""
AliExpress data service — simulated in v1.
Returns plausible supplier/pricing data based on product name.
Replace with real AliExpress API or scraper in v2.
"""
import random
import hashlib


def _seed_from_name(name: str) -> int:
    return int(hashlib.md5(("ali" + name.lower()).encode()).hexdigest(), 16) % 10000


def get_aliexpress_data(product_name: str) -> dict:
    """
    Returns simulated AliExpress supplier data for a product.

    Returns:
        {
            "supplier_count": int,            # number of suppliers found
            "price_min": float,               # lowest supplier price (USD)
            "price_max": float,               # highest supplier price (USD)
            "avg_rating": float,              # average supplier rating (1-5)
            "avg_shipping_days": int,         # average shipping time
            "margin_potential_score": int     # 0-100, higher = better margins
        }
    """
    rng = random.Random(_seed_from_name(product_name))

    supplier_count = rng.randint(5, 300)
    price_min = round(rng.uniform(2.0, 25.0), 2)
    price_max = round(price_min * rng.uniform(1.5, 4.0), 2)
    avg_rating = round(rng.uniform(3.5, 4.9), 1)
    shipping_days = rng.randint(7, 30)

    # Higher margin potential if price is low and suppliers are plentiful
    margin_score = min(100, int((25 / max(price_min, 1)) * 20 + (supplier_count / 300) * 30 + rng.randint(10, 40)))

    return {
        "supplier_count": supplier_count,
        "price_min": price_min,
        "price_max": price_max,
        "avg_rating": avg_rating,
        "avg_shipping_days": shipping_days,
        "margin_potential_score": margin_score,
    }
