# WinPilot — Implementation Tasks

## Task 1 — Project Scaffold
- [ ] Create folder structure (frontend/, backend/)
- [ ] Create backend/requirements.txt
- [ ] Create backend/.env.example
- [ ] Create vercel.json
- [ ] Create README.md

## Task 2 — Backend: Schemas + Claude Service
- [ ] Define Pydantic models in backend/models/schemas.py
- [ ] Build Claude API wrapper in backend/services/claude.py
- [ ] Write validator prompt in backend/prompts/validator_prompt.py
- [ ] Write hunter prompt in backend/prompts/hunter_prompt.py

## Task 3 — Backend: Simulated Data Services
- [ ] backend/services/trends.py — return simulated trend data
- [ ] backend/services/meta_ads.py — return simulated ad competition data
- [ ] backend/services/aliexpress.py — return simulated price/supplier data

## Task 4 — Backend: API Endpoints
- [ ] POST /validate in backend/routers/validator.py
- [ ] POST /hunt in backend/routers/hunter.py
- [ ] Wire up routers in backend/main.py with CORS enabled

## Task 5 — Frontend: Product Validator UI
- [ ] Build validator.html with dynamic product input form (up to 5 slots)
- [ ] Build validator.js — form validation, POST to /validate, render results
- [ ] Build result cards with score bars and verdict badges

## Task 6 — Frontend: Product Hunter UI
- [ ] Build hunter.html with niche questionnaire form
- [ ] Build hunter.js — POST to /hunt, render 5 suggestions with checkboxes
- [ ] Wire selection → /validate pipeline, render ranked results

## Task 7 — Frontend: Shared UI + Landing Page
- [ ] Build index.html with tab/nav to Validator and Hunter
- [ ] Build css/styles.css — clean, modern dark theme
- [ ] Build js/ui.js — shared helpers (loaders, toasts, score bars)

## Task 8 — Deployment Config
- [ ] Configure vercel.json for static frontend
- [ ] Add Render/Railway start command to README
- [ ] Document environment variables
