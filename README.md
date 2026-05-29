# WinPilot 🚀

AI-powered dropshipping product research tool. Validate products and discover trending winners using Claude AI.

## Features

- **Product Validator** — submit up to 5 products, get AI scores across trend, competition, margin, and saturation
- **Product Hunter** — describe your niche, get 5 trending product suggestions, validate the best ones
- Powered by Claude Haiku (fast scoring) and Claude Sonnet (deep discovery)

---

## Project Structure

```
winpilot/
├── frontend/          # Static HTML/CSS/JS — deploy to Vercel
│   ├── index.html
│   ├── validator.html
│   ├── hunter.html
│   ├── css/styles.css
│   └── js/
│       ├── ui.js
│       ├── validator.js
│       └── hunter.js
│
├── backend/           # FastAPI — deploy to Render or Railway
│   ├── main.py
│   ├── routers/
│   ├── services/
│   ├── models/
│   ├── prompts/
│   └── requirements.txt
│
├── vercel.json
└── README.md
```

---

## Local Development

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Start the server
uvicorn main:app --reload --port 8000
```

API will be available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

### Frontend

Open `frontend/index.html` directly in a browser, or use a local server:

```bash
# Using Python
python -m http.server 5500 --directory frontend

# Using VS Code Live Server extension — right-click index.html → Open with Live Server
```

Make sure the backend is running on port 8000 before using the app.

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | ✅ | — | Your Anthropic API key |
| `CLAUDE_HAIKU_MODEL` | ❌ | `claude-haiku-4-5` | Model for product scoring |
| `CLAUDE_SONNET_MODEL` | ❌ | `claude-sonnet-4-5` | Model for product discovery |
| `ALLOWED_ORIGINS` | ❌ | `http://localhost:3000,...` | Comma-separated CORS origins |

---

## Deployment

### Frontend → Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from project root
vercel --prod
```

### Backend → Render

1. Create a new **Web Service** on [render.com](https://render.com)
2. Connect your GitHub repo
3. Set:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add `ANTHROPIC_API_KEY` in Environment Variables
5. Update `ALLOWED_ORIGINS` to your Vercel frontend URL

### Backend → Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

railway login
railway init
railway up
```

Set environment variables in the Railway dashboard.

---

## API Reference

### `POST /api/validate`

Validate up to 5 products.

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
      "image_url": "...",
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

### `POST /api/hunt`

Discover 5 trending products for a niche.

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

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JS |
| Backend | Python 3.11+, FastAPI |
| AI | Anthropic Claude API |
| Frontend Deploy | Vercel |
| Backend Deploy | Render / Railway |

---

## Roadmap

- [ ] Real Google Trends integration via `pytrends`
- [ ] Real Meta Ad Library API
- [ ] AliExpress product search API
- [ ] Session history (localStorage)
- [ ] Export results as PDF/CSV
- [ ] Saved product watchlist
