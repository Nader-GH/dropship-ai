from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from enum import Enum


# ── Shared ────────────────────────────────────────────────────────────────────

class Verdict(str, Enum):
    worth_testing = "worth_testing"
    proceed_with_caution = "proceed_with_caution"
    not_recommended = "not_recommended"


# ── Validator ─────────────────────────────────────────────────────────────────

class ProductInput(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    image_url: Optional[str] = Field(None)


class ValidateRequest(BaseModel):
    products: List[ProductInput] = Field(..., min_length=1, max_length=5)


class ProductScores(BaseModel):
    trend_score: int = Field(..., ge=0, le=100)
    ad_competition: int = Field(..., ge=0, le=100)
    margin_estimate: int = Field(..., ge=0, le=100)
    saturation_level: int = Field(..., ge=0, le=100)


class ProductResult(BaseModel):
    name: str
    image_url: Optional[str]
    scores: ProductScores
    composite_score: int
    verdict: Verdict
    summary: str


class ValidateResponse(BaseModel):
    results: List[ProductResult]


# ── Hunter ────────────────────────────────────────────────────────────────────

class HuntRequest(BaseModel):
    niche: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=2, max_length=60)
    budget: str = Field(..., description="Monthly ad budget range, e.g. '500-1000'")
    price_range: Optional[str] = Field(None, description="Preferred product price range, e.g. '20-60'")
    avoid: Optional[str] = Field(None, description="Categories or keywords to avoid")


class ProductSuggestion(BaseModel):
    name: str
    description: str
    why_trending: str
    estimated_price: str


class HuntResponse(BaseModel):
    suggestions: List[ProductSuggestion]
