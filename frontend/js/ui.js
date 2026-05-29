/**
 * ui.js — shared UI helpers for WinPilot
 * Used by both validator.js and hunter.js
 */

const API_BASE = "http://localhost:8000/api";

// ── Verdict helpers ────────────────────────────────────────────────────────

const VERDICT_CONFIG = {
  worth_testing: {
    label: "Worth Testing Ads",
    emoji: "✅",
    className: "verdict--green",
  },
  proceed_with_caution: {
    label: "Proceed with Caution",
    emoji: "⚠️",
    className: "verdict--yellow",
  },
  not_recommended: {
    label: "Not Recommended",
    emoji: "❌",
    className: "verdict--red",
  },
};

function getVerdictConfig(verdict) {
  return VERDICT_CONFIG[verdict] || VERDICT_CONFIG["proceed_with_caution"];
}

// ── Score bar ──────────────────────────────────────────────────────────────

/**
 * Renders a labelled score bar.
 * @param {string} label
 * @param {number} score  0–100
 * @param {boolean} inverted  if true, high score = bad (red), low = good (green)
 */
function renderScoreBar(label, score, inverted = false) {
  const pct = Math.min(100, Math.max(0, score));
  let colorClass;
  const effectiveScore = inverted ? 100 - pct : pct;
  if (effectiveScore >= 70) colorClass = "bar--green";
  else if (effectiveScore >= 45) colorClass = "bar--yellow";
  else colorClass = "bar--red";

  return `
    <div class="score-row">
      <span class="score-label">${label}</span>
      <div class="score-bar-track">
        <div class="score-bar-fill ${colorClass}" style="width: ${pct}%"></div>
      </div>
      <span class="score-value">${pct}</span>
    </div>
  `;
}

// ── Result card ────────────────────────────────────────────────────────────

/**
 * Builds a full product result card HTML string.
 * @param {object} result  ProductResult from /validate
 * @param {number|null} rank  optional rank badge (1 = top pick)
 */
function buildResultCard(result, rank = null) {
  const vc = getVerdictConfig(result.verdict);
  const { trend_score, ad_competition, margin_estimate, saturation_level } = result.scores;

  const rankBadge = rank
    ? `<div class="rank-badge rank-badge--${rank === 1 ? "gold" : rank === 2 ? "silver" : "bronze"}">#${rank}</div>`
    : "";

  const image = result.image_url
    ? `<img src="${escapeHtml(result.image_url)}" alt="${escapeHtml(result.name)}" class="product-image" onerror="this.style.display='none'" />`
    : `<div class="product-image-placeholder">📦</div>`;

  return `
    <div class="result-card ${vc.className}">
      ${rankBadge}
      <div class="result-card__header">
        ${image}
        <div class="result-card__title-block">
          <h3 class="result-card__name">${escapeHtml(result.name)}</h3>
          <div class="verdict-badge ${vc.className}">
            ${vc.emoji} ${vc.label}
          </div>
          <div class="composite-score">
            <span class="composite-score__number">${result.composite_score}</span>
            <span class="composite-score__label">/ 100</span>
          </div>
        </div>
      </div>

      <div class="score-bars">
        ${renderScoreBar("Trend Score", trend_score)}
        ${renderScoreBar("Margin Estimate", margin_estimate)}
        ${renderScoreBar("Ad Competition", ad_competition, true)}
        ${renderScoreBar("Saturation Level", saturation_level, true)}
      </div>

      <p class="result-summary">${escapeHtml(result.summary)}</p>
    </div>
  `;
}

// ── Toast notifications ────────────────────────────────────────────────────

function showToast(message, type = "error") {
  const existing = document.getElementById("toast");
  if (existing) existing.remove();

  const toast = document.createElement("div");
  toast.id = "toast";
  toast.className = `toast toast--${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => toast.classList.add("toast--visible"), 10);
  setTimeout(() => {
    toast.classList.remove("toast--visible");
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// ── Loading state ──────────────────────────────────────────────────────────

function showLoading(loadingEl) {
  loadingEl.classList.remove("hidden");
}

function hideLoading(loadingEl) {
  loadingEl.classList.add("hidden");
}

// ── Utility ────────────────────────────────────────────────────────────────

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
