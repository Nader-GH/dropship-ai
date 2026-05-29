/**
 * hunter.js — Product Hunter page logic
 */

const MAX_SELECTIONS = 3;
let suggestions = [];
let selectedIndexes = new Set();

const huntBtn = document.getElementById("hunt-btn");
const loadingEl = document.getElementById("loading");
const stepSuggestions = document.getElementById("step-suggestions");
const suggestionsGrid = document.getElementById("suggestions-grid");
const selectionCounter = document.getElementById("selection-counter");
const validateSelectedBtn = document.getElementById("validate-selected-btn");
const stepResults = document.getElementById("step-results");
const resultsGrid = document.getElementById("results-grid");

// ── Hunt ───────────────────────────────────────────────────────────────────

huntBtn.addEventListener("click", async () => {
  const niche = document.getElementById("niche").value.trim();
  const country = document.getElementById("country").value.trim();
  const budget = document.getElementById("budget").value;
  const priceRange = document.getElementById("price-range").value.trim();
  const avoid = document.getElementById("avoid").value.trim();

  if (!niche) {
    showToast("Please enter your target niche.");
    document.getElementById("niche").focus();
    return;
  }
  if (!country) {
    showToast("Please enter your target country.");
    document.getElementById("country").focus();
    return;
  }

  huntBtn.disabled = true;
  stepSuggestions.classList.add("hidden");
  stepResults.classList.add("hidden");
  showLoading(loadingEl);

  try {
    const res = await fetch(`${API_BASE}/hunt`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        niche,
        country,
        budget,
        price_range: priceRange || null,
        avoid: avoid || null,
      }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Unknown error" }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }

    const data = await res.json();
    suggestions = data.suggestions;
    selectedIndexes.clear();
    renderSuggestions(suggestions);
  } catch (err) {
    showToast(`Hunt failed: ${err.message}`);
  } finally {
    hideLoading(loadingEl);
    huntBtn.disabled = false;
  }
});

// ── Render suggestions ─────────────────────────────────────────────────────

function renderSuggestions(items) {
  suggestionsGrid.innerHTML = items
    .map(
      (s, i) => `
    <div class="suggestion-card" data-index="${i}">
      <div class="suggestion-card__header">
        <span class="suggestion-number">${i + 1}</span>
        <h3 class="suggestion-name">${escapeHtml(s.name)}</h3>
        <label class="checkbox-label" aria-label="Select ${escapeHtml(s.name)}">
          <input type="checkbox" class="suggestion-checkbox" data-index="${i}" />
          <span class="checkbox-custom"></span>
        </label>
      </div>
      <p class="suggestion-desc">${escapeHtml(s.description)}</p>
      <div class="suggestion-meta">
        <div class="meta-row">
          <span class="meta-icon">📈</span>
          <span>${escapeHtml(s.why_trending)}</span>
        </div>
        <div class="meta-row">
          <span class="meta-icon">💰</span>
          <span>${escapeHtml(s.estimated_price)}</span>
        </div>
      </div>
    </div>
  `
    )
    .join("");

  // Attach checkbox listeners
  suggestionsGrid.querySelectorAll(".suggestion-checkbox").forEach((cb) => {
    cb.addEventListener("change", onCheckboxChange);
  });

  stepSuggestions.classList.remove("hidden");
  stepSuggestions.scrollIntoView({ behavior: "smooth" });
  updateSelectionCounter();
}

function onCheckboxChange(e) {
  const idx = parseInt(e.target.dataset.index);
  const card = e.target.closest(".suggestion-card");

  if (e.target.checked) {
    if (selectedIndexes.size >= MAX_SELECTIONS) {
      e.target.checked = false;
      showToast(`You can only select up to ${MAX_SELECTIONS} products.`, "warning");
      return;
    }
    selectedIndexes.add(idx);
    card.classList.add("suggestion-card--selected");
  } else {
    selectedIndexes.delete(idx);
    card.classList.remove("suggestion-card--selected");
  }

  updateSelectionCounter();
}

function updateSelectionCounter() {
  const count = selectedIndexes.size;
  selectionCounter.textContent = `${count} / ${MAX_SELECTIONS} selected`;
  validateSelectedBtn.disabled = count === 0;
}

// ── Validate selected ──────────────────────────────────────────────────────

validateSelectedBtn.addEventListener("click", async () => {
  if (selectedIndexes.size === 0) return;

  const selected = [...selectedIndexes].map((i) => ({
    name: suggestions[i].name,
    description: suggestions[i].description,
    image_url: null,
  }));

  validateSelectedBtn.disabled = true;
  stepResults.classList.add("hidden");
  showLoading(loadingEl);

  try {
    const res = await fetch(`${API_BASE}/validate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ products: selected }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Unknown error" }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }

    const data = await res.json();

    // Sort by composite score descending for ranking
    const ranked = [...data.results].sort((a, b) => b.composite_score - a.composite_score);
    renderRankedResults(ranked);
  } catch (err) {
    showToast(`Validation failed: ${err.message}`);
  } finally {
    hideLoading(loadingEl);
    validateSelectedBtn.disabled = selectedIndexes.size === 0;
  }
});

// ── Render ranked results ──────────────────────────────────────────────────

function renderRankedResults(results) {
  resultsGrid.innerHTML = results.map((r, i) => buildResultCard(r, i + 1)).join("");
  stepResults.classList.remove("hidden");
  stepResults.scrollIntoView({ behavior: "smooth" });
}
