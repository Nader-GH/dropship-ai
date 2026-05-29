# Requirements Document

## Introduction

WinPilot is an AI-powered dropshipping product research tool designed for solo dropshippers who want to validate products before spending money on ads. The tool aggregates real market data from Google Trends, Meta Ad Library, TikTok, and AliExpress, then uses Claude AI to score each product and deliver a clear verdict: test it or skip it.

The application has two core features:
- **Product Validator**: the user submits up to 5 products manually (name, description, image URL) and receives a scored analysis for each.
- **Product Hunter**: the user describes their niche and target market, the AI suggests 5 trending products, the user picks up to 3, and the system scores and ranks them.

The app is stateless (no database, no login), runs on a plain HTML/CSS/JS frontend deployed to Vercel, and a Python FastAPI backend deployed to Railway or Render. The AI brain is the Anthropic Claude API (claude-haiku for speed, claude-sonnet for deep analysis).

---

## Glossary

- **WinPilot**: The full application described in this document.
- **Product_Validator**: The feature that accepts user-submitted products and returns scored analysis cards.
- **Product_Hunter**: The feature that suggests trending products based on user niche/market input and scores the selected ones.
- **Score_Card**: The structured output per product containing trend score, ad competition level, estimated profit margin, saturation level, and a final verdict.
- **Verdict**: A binary recommendation — "Test It" or "Skip It" — accompanied by a short explanation.
- **Analysis_Engine**: The backend service responsible for orchestrating data collection and Claude AI calls to produce a Score_Card.
- **Data_Aggregator**: The backend component that fetches data from Google Trends, Meta Ad Library, TikTok, and AliExpress.
- **Claude_Client**: The backend component that communicates with the Anthropic Claude API.
- **Session**: A single browser session; no data persists between sessions.
- **Niche**: A product category or market segment provided by the user in the Product Hunter flow.
- **Target_Country**: The geographic market the dropshipper intends to sell in.

---

## Requirements

### Requirement 1: Product Input Form

**User Story:** As a dropshipper, I want to submit up to 5 products with a name, description, and image URL, so that WinPilot can research and score each one for me.

#### Acceptance Criteria

1. THE Product_Validator SHALL provide an input form that accepts between 1 and 5 products per submission.
2. WHEN a user submits a product, THE Product_Validator SHALL require a product name (non-empty string, maximum 100 characters).
3. WHEN a user submits a product, THE Product_Validator SHALL require a product description (non-empty string, maximum 500 characters).
4. WHERE an image URL is provided, THE Product_Validator SHALL accept it as an optional field and validate that it is a well-formed URL.
5. WHEN a user attempts to submit more than 5 products, THE Product_Validator SHALL prevent submission and display an error message indicating the 5-product limit.
6. WHEN a required field is empty at submission time, THE Product_Validator SHALL highlight the invalid field and display a descriptive validation message without submitting the form.

---

### Requirement 2: Single Product Analysis

**User Story:** As a dropshipper, I want the system to analyze a submitted product using real market data and AI, so that I receive an objective score and verdict instead of guessing.

#### Acceptance Criteria

1. WHEN a valid product is submitted, THE Analysis_Engine SHALL initiate an analysis pipeline for that product within 2 seconds of receiving the request.
2. WHEN the analysis pipeline runs, THE Data_Aggregator SHALL query Google Trends for the product's search interest over the past 90 days.
3. WHEN the analysis pipeline runs, THE Data_Aggregator SHALL query the Meta Ad Library for active ads related to the product.
4. WHEN the analysis pipeline runs, THE Data_Aggregator SHALL query TikTok for recent content volume and engagement signals related to the product.
5. WHEN the analysis pipeline runs, THE Data_Aggregator SHALL query AliExpress for supplier availability and approximate pricing for the product.
6. WHEN all data sources have been queried, THE Claude_Client SHALL send the aggregated data to the Claude API using the claude-sonnet model to produce a Score_Card.
7. WHEN the Claude API returns a response, THE Analysis_Engine SHALL parse the response into a structured Score_Card containing: trend score (0–100), ad competition level (Low / Medium / High), estimated profit margin (percentage range), saturation level (Low / Medium / High), and a Verdict with a short explanation (maximum 100 words).
8. IF a data source query fails, THEN THE Data_Aggregator SHALL log the failure and continue the pipeline using the available data, marking the missing data source as unavailable in the Score_Card.
9. WHEN the Score_Card is ready, THE Analysis_Engine SHALL return it to the frontend within 30 seconds of the original submission.

---

### Requirement 3: Score Card Display

**User Story:** As a dropshipper, I want to see a clear, visual score card for each analyzed product, so that I can quickly understand whether to test it or skip it.

#### Acceptance Criteria

1. WHEN a Score_Card is received, THE Product_Validator SHALL render it as a visual card in the browser without a page reload.
2. THE Product_Validator SHALL display the product name and image (if provided) at the top of each Score_Card.
3. THE Product_Validator SHALL display the trend score as a numeric value out of 100 with a visual indicator (e.g., progress bar or color-coded badge).
4. THE Product_Validator SHALL display the ad competition level (Low / Medium / High) with a corresponding color indicator (green / yellow / red).
5. THE Product_Validator SHALL display the estimated profit margin as a percentage range.
6. THE Product_Validator SHALL display the saturation level (Low / Medium / High) with a corresponding color indicator (green / yellow / red).
7. THE Product_Validator SHALL display the Verdict prominently as either "Test It" or "Skip It" with the short explanation below it.
8. IF a data source was marked unavailable, THEN THE Product_Validator SHALL display a notice on the Score_Card indicating which data source was unavailable.

---

### Requirement 4: Multi-Product Batch Analysis

**User Story:** As a dropshipper, I want to submit multiple products at once and receive all their score cards, so that I can compare them side by side.

#### Acceptance Criteria

1. WHEN a user submits between 2 and 5 products, THE Analysis_Engine SHALL analyze each product independently and in parallel where infrastructure allows.
2. WHEN all Score_Cards for a batch are ready, THE Product_Validator SHALL display them together on the same page in the order they were submitted.
3. WHEN a batch analysis is in progress, THE Product_Validator SHALL display a loading indicator for each product that has not yet received its Score_Card.
4. IF one product in a batch fails analysis, THEN THE Analysis_Engine SHALL return an error Score_Card for that product and continue processing the remaining products.

---

### Requirement 5: Product Hunter — Niche and Market Input

**User Story:** As a dropshipper, I want to describe my niche and target country so that WinPilot can suggest trending products relevant to my market.

#### Acceptance Criteria

1. THE Product_Hunter SHALL provide an input form that accepts a niche description (non-empty string, maximum 200 characters).
2. THE Product_Hunter SHALL provide a target country selector with a list of at least the 20 most common dropshipping destination countries.
3. WHEN a user submits the niche form, THE Product_Hunter SHALL require both the niche description and the target country before proceeding.
4. WHEN a required field is empty at submission time, THE Product_Hunter SHALL highlight the invalid field and display a descriptive validation message without submitting the form.

---

### Requirement 6: AI-Powered Product Suggestions

**User Story:** As a dropshipper, I want the AI to suggest 5 trending products based on my niche and target country, so that I have data-backed product ideas to evaluate.

#### Acceptance Criteria

1. WHEN a valid niche form is submitted, THE Claude_Client SHALL send the niche description and target country to the Claude API using the claude-haiku model to generate exactly 5 product suggestions.
2. WHEN the Claude API returns suggestions, THE Product_Hunter SHALL display each suggestion as a selectable card showing the product name and a brief rationale (maximum 50 words).
3. WHEN suggestions are displayed, THE Product_Hunter SHALL allow the user to select between 1 and 3 products for scoring.
4. WHEN a user attempts to select more than 3 products, THE Product_Hunter SHALL prevent the additional selection and display a message indicating the 3-product limit.
5. IF the Claude API fails to return suggestions, THEN THE Product_Hunter SHALL display an error message and provide a retry option.
6. WHEN the Claude API returns suggestions, THE Product_Hunter SHALL display them within 15 seconds of the niche form submission.

---

### Requirement 7: Product Hunter Scoring and Ranking

**User Story:** As a dropshipper, I want the selected products from the Product Hunter to be scored and ranked, so that I know which one to prioritize testing.

#### Acceptance Criteria

1. WHEN a user confirms their product selection (1–3 products), THE Analysis_Engine SHALL run the full analysis pipeline (as defined in Requirement 2) for each selected product.
2. WHEN all Score_Cards for the selected products are ready, THE Product_Hunter SHALL display them ranked in descending order by total score.
3. THE Product_Hunter SHALL visually distinguish the top-ranked product (e.g., a "Top Pick" badge).
4. WHEN a batch analysis is in progress, THE Product_Hunter SHALL display a loading indicator for each product that has not yet received its Score_Card.

---

### Requirement 8: Stateless Session Behavior

**User Story:** As a dropshipper, I want the app to work without requiring me to create an account, so that I can use it immediately without friction.

#### Acceptance Criteria

1. THE WinPilot SHALL operate without any user authentication or account creation.
2. THE WinPilot SHALL not persist any user-submitted data, analysis results, or session state to a database or external storage.
3. WHEN a user refreshes or closes the browser, THE WinPilot SHALL discard all current session data.
4. WHEN a new browser session starts, THE WinPilot SHALL present a clean, empty state with no data from previous sessions.

---

### Requirement 9: API Cost and Performance Constraints

**User Story:** As a solo dropshipper on a tight budget, I want the app to stay within a $30/month operating cost, so that it remains affordable to run.

#### Acceptance Criteria

1. WHEN performing product suggestions in the Product Hunter, THE Claude_Client SHALL use the claude-haiku model to minimize token cost.
2. WHEN performing deep product analysis in the Analysis_Engine, THE Claude_Client SHALL use the claude-sonnet model for quality scoring.
3. THE Analysis_Engine SHALL limit each Claude API call to a maximum prompt size of 4000 tokens to control cost per analysis.
4. IF the total estimated monthly API cost exceeds $30 based on usage patterns, THEN THE Analysis_Engine SHALL log a cost warning to the server console.

---

### Requirement 10: Error Handling and User Feedback

**User Story:** As a dropshipper, I want clear feedback when something goes wrong, so that I know what happened and can try again.

#### Acceptance Criteria

1. IF the backend API is unreachable, THEN THE Product_Validator SHALL display a user-friendly error message and a retry button within 10 seconds of the failed request.
2. IF the backend API is unreachable, THEN THE Product_Hunter SHALL display a user-friendly error message and a retry button within 10 seconds of the failed request.
3. IF an analysis takes longer than 30 seconds, THEN THE Analysis_Engine SHALL return a timeout error response, and THE Product_Validator SHALL display a timeout message with a retry option.
4. WHEN an unexpected server error occurs, THE Analysis_Engine SHALL return an error response with a human-readable message and an HTTP status code of 500.
5. WHEN a validation error occurs on the backend, THE Analysis_Engine SHALL return an error response with a human-readable message and an HTTP status code of 422.
