"""
Google Trends data service — simulated in v1.
Returns plausible trend data based on product name/description keywords.
Replace the body of get_trend_data() with a real pytrends call in v2.
"""
import random
import hashlib


def _seed_from_name(name: str) -> int:
    """Deterministic seed so the same product always gets the same mock score."""
    return int(hashlib.md5(name.lower().encode()).hexdigest(), 16) % 10000


def get_trend_data(product_name: str, description: str) -> dict:
    """
    Returns simulated Google Trends data for a product.

    Returns:
        {
            "interest_score": int (0-100),   # current search interest
            "trend_direction": str,           # "rising" | "stable" | "declining"
            "peak_months": list[str],         # months with highest interest
            "related_queries": list[str]      # related search terms
        }
    """
    rng = random.Random(_seed_from_name(product_name))

    interest_score = rng.randint(30, 95)

    if interest_score >= 70:
        direction = "rising"
    elif interest_score >= 45:
        direction = "stable"
    else:
        direction = "declining"

    all_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    peak_months = rng.sample(all_months, k=rng.randint(2, 4))

    words = (product_name + " " + description).lower().split()
    keywords = [w for w in words if len(w) > 4][:3]
    related = [f"{kw} buy online" for kw in keywords] or ["dropshipping products", "trending items"]

    return {
        "interest_score": interest_score,
        "trend_direction": direction,
        "peak_months": sorted(peak_months, key=lambda m: all_months.index(m)),
        "related_queries": related,
    }
