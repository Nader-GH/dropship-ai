# WinPilot — Technical Design

## Folder Structure

```
winpilot/
├── frontend/
│   ├── index.html          # Landing page + tab navigation
│   ├── validator.html      # Product Validator page
│   ├── hunter.html         # Product Hunter page
│   ├── css/
│   │   └── styles.css      # Global styles
│   └── js/
│       ├── validator.js    # Validator form logic + API calls
│       ├── hunter.js       # Hunter questionnaire + API calls
│       └── ui.js           # Shared UI helpers (cards, loaders, toasts)
│
├── backend/
│   ├── main.py             # FastAPI app entry point
│   ├── routers/
│   │   ├── validator.py    # POST /validate endpoint
│   │   └── hunter.py       # POST /hunt endpoint
│   ├── services/
│   │   ├── claude.py       # Claude API wrapper (haiku + sonnet)
│   │   ├── trends.py       # Google Trends data (simulated v1)
│   │   ├── meta_ads.py     # Meta Ad Library data (simulated v1)
│   │   └── aliexpress.py   # AliExpress data (simulated v1)
│   ├── models/
│   │   └── schemas.py      # Pydantic request/response models
│   ├── prompts/
│   │   ├── validator_prompt.py   # Claude prompt for scoring
│   │   └── hunter_prompt.py     # Claude prompt for product discovery
│   ├── requirements.txt
│   └── .env.example
│
├── vercel.json             # Vercel config for frontend
└── README.md
```

---

## API Design

### POST /validate
**Request:**
```json
{
  "products": [
    {
      "name": "Magnetic Phone Mount",
      "description": "Strong magnetic car mount for all phones",
      "image_url": "https://example.com/img.jpg"
    }
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "name": "Magnetic Phone Mount",
      "image_url": "https://example.com/img.jpg",
      "scores": {
        "trend_score": 78,
        "ad_competition": 62,
        "margin_estimate": 71,
        "saturation_level": 45
      },
      "composite_score": 74,
      "verdict": "worth_testing",
      "summary": "Strong upward trend with manageable competition..."
    }
  ]
}
```

### POST /hunt
**Request:**
```json
{
  "niche": "home fitness",
  "country": "US",
  "budget": "500-1000",
  "price_range": "20-60",
  "avoid": "supplements"
}
```

**Response:**
```json
{
  "suggestions": [
    {
      "name": "Resistance Band Set",
      "description": "...",
      "why_trending": "...",
      "estimated_price": "$8–$15 AliExpress / sell at $35–$45"
    }
  ]
}
```

---

## Claude Prompt Strategy

### Validator Prompt (Haiku)
- System: "You are a dropshipping product analyst..."
- User: structured product data + simulated research data
- Output: strict JSON with scores + verdict + summary

### Hunter Prompt (Sonnet)
- System: "You are a dropshipping trend expert..."
- User: niche questionnaire answers
- Output: JSON array of 5 product suggestions

---

## Scoring Logic

| Score | Verdict |
|-------|---------|
| 70–100 | ✅ Worth testing ads |
| 45–69 | ⚠️ Proceed with caution |
| 0–44 | ❌ Not recommended |

Composite score = weighted average:
- Trend Score: 35%
- Margin Estimate: 30%
- Ad Competition (inverted): 20%
- Saturation Level (inverted): 15%
