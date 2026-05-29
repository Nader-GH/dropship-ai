from fastapi import APIRouter, HTTPException
from models.schemas import HuntRequest, HuntResponse, ProductSuggestion
from services.claude import call_sonnet
from prompts.hunter_prompt import HUNTER_SYSTEM, build_hunter_prompt

router = APIRouter()


@router.post("/hunt", response_model=HuntResponse)
async def hunt_products(request: HuntRequest):
    """
    Use Claude Sonnet to suggest 5 trending products based on niche questionnaire.
    """
    user_prompt = build_hunter_prompt(
        niche=request.niche,
        country=request.country,
        budget=request.budget,
        price_range=request.price_range,
        avoid=request.avoid,
    )

    try:
        data = call_sonnet(HUNTER_SYSTEM, user_prompt)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"Claude parsing error: {e}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Claude API error: {e}")

    suggestions = [
        ProductSuggestion(
            name=s["name"],
            description=s["description"],
            why_trending=s["why_trending"],
            estimated_price=s["estimated_price"],
        )
        for s in data.get("suggestions", [])
    ]

    return HuntResponse(suggestions=suggestions)
