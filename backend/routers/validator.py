import asyncio
from fastapi import APIRouter, HTTPException
from models.schemas import ValidateRequest, ValidateResponse, ProductResult, ProductScores, Verdict
from services.trends import get_trend_data
from services.meta_ads import get_ad_competition_data
from services.aliexpress import get_aliexpress_data
from services.claude import call_haiku
from prompts.validator_prompt import VALIDATOR_SYSTEM, build_validator_prompt

router = APIRouter()


def _analyze_single_product(name: str, description: str, image_url: str | None) -> ProductResult:
    """Run research + Claude scoring for one product (synchronous)."""
    trends = get_trend_data(name, description)
    meta_ads = get_ad_competition_data(name)
    aliexpress = get_aliexpress_data(name)

    user_prompt = build_validator_prompt(name, description, trends, meta_ads, aliexpress)

    try:
        data = call_haiku(VALIDATOR_SYSTEM, user_prompt)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"Claude parsing error: {e}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Claude API error: {e}")

    scores = ProductScores(
        trend_score=int(data["trend_score"]),
        ad_competition=int(data["ad_competition"]),
        margin_estimate=int(data["margin_estimate"]),
        saturation_level=int(data["saturation_level"]),
    )

    return ProductResult(
        name=name,
        image_url=image_url,
        scores=scores,
        composite_score=int(data["composite_score"]),
        verdict=Verdict(data["verdict"]),
        summary=data["summary"],
    )


@router.post("/validate", response_model=ValidateResponse)
async def validate_products(request: ValidateRequest):
    """
    Validate up to 5 products in parallel.
    Each product is scored by Claude Haiku using simulated research data.
    """
    loop = asyncio.get_event_loop()

    tasks = [
        loop.run_in_executor(
            None,
            _analyze_single_product,
            p.name,
            p.description,
            p.image_url,
        )
        for p in request.products
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    processed = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            raise HTTPException(
                status_code=502,
                detail=f"Error analyzing product '{request.products[i].name}': {result}",
            )
        processed.append(result)

    return ValidateResponse(results=processed)
