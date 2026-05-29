VALIDATOR_SYSTEM = """You are an expert dropshipping product analyst with deep knowledge of e-commerce trends, Facebook/Meta advertising, and AliExpress sourcing.

Your job is to analyze a product using the research data provided and return a structured JSON score.

You MUST respond with ONLY valid JSON — no markdown, no explanation, no extra text.

The JSON must follow this exact structure:
{
  "trend_score": <integer 0-100>,
  "ad_competition": <integer 0-100>,
  "margin_estimate": <integer 0-100>,
  "saturation_level": <integer 0-100>,
  "composite_score": <integer 0-100>,
  "verdict": <"worth_testing" | "proceed_with_caution" | "not_recommended">,
  "summary": <string, 2-3 sentences explaining the verdict>
}

Scoring guidelines:
- trend_score: 100 = explosive growth, 0 = dying trend
- ad_competition: 100 = extremely competitive (bad for new entrants), 0 = no competition
- margin_estimate: 100 = excellent margins (>60%), 0 = no margin
- saturation_level: 100 = completely saturated market, 0 = untapped

Composite score formula (apply this exactly):
composite_score = round(
  trend_score * 0.35 +
  margin_estimate * 0.30 +
  (100 - ad_competition) * 0.20 +
  (100 - saturation_level) * 0.15
)

Verdict thresholds:
- 70-100 → "worth_testing"
- 45-69  → "proceed_with_caution"
- 0-44   → "not_recommended"
"""


def build_validator_prompt(product_name: str, description: str, trends: dict, meta_ads: dict, aliexpress: dict) -> str:
    return f"""Analyze this dropshipping product:

PRODUCT NAME: {product_name}
DESCRIPTION: {description}

GOOGLE TRENDS DATA:
- Current interest score: {trends['interest_score']}/100
- Trend direction: {trends['trend_direction']}
- Peak months: {', '.join(trends['peak_months'])}
- Related queries: {', '.join(trends['related_queries'])}

META AD LIBRARY DATA:
- Estimated active ads: {meta_ads['active_ads_estimate']}
- Competition score: {meta_ads['competition_score']}/100
- Top ad formats: {', '.join(meta_ads['top_ad_formats'])}
- Avg engagement rate: {meta_ads['avg_engagement_rate']}%

ALIEXPRESS DATA:
- Supplier count: {aliexpress['supplier_count']}
- Price range: ${aliexpress['price_min']} – ${aliexpress['price_max']}
- Avg supplier rating: {aliexpress['avg_rating']}/5
- Avg shipping time: {aliexpress['avg_shipping_days']} days
- Margin potential score: {aliexpress['margin_potential_score']}/100

Based on this data, provide your analysis as JSON only."""
