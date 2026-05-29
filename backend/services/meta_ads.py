"""
Meta Ad Library data service — simulated in v1.
Returns plausible ad competition data based on product name.
Replace with real Meta Ad Library API calls in v2.
"""
import random
import hashlib


def _seed_from_name(name: str) -> int:
    return int(hashlib.md5(("meta" + name.lower()).encode()).hexdigest(), 16) % 10000


def get_ad_competition_data(product_name: str) -> dict:
    """
    Returns simulated Meta Ad Library data for a product.

    Returns:
        {
            "active_ads_estimate": int,       # estimated number of active ads
            "competition_score": int (0-100), # 100 = extremely competitive
            "top_ad_formats": list[str],      # dominant ad formats
            "avg_engagement_rate": float      # estimated engagement %
        }
    """
    rng = random.Random(_seed_from_name(product_name))

    active_ads = rng.randint(50, 5000)
    competition_score = min(100, int(active_ads / 50))

    formats = rng.sample(["Video", "Carousel", "Single Image", "Collection", "Stories"], k=rng.randint(2, 3))
    engagement = round(rng.uniform(0.8, 4.5), 2)

    return {
        "active_ads_estimate": active_ads,
        "competition_score": competition_score,
        "top_ad_formats": formats,
        "avg_engagement_rate": engagement,
    }
