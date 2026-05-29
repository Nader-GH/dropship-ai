/**
 * validator.js — Product Validator page logic
 */

const MAX_SLOTS = 5;
let slotCount = 0;

const slotsContainer = document.getElementById("product-slots");
const addBtn = document.getElementById("add-product-btn");
const validateBtn = document.getElementById("validate-btn");
const slotCounter = document.getElementById("slot-counter");
const loadingEl = document.getElementById("loading");
const resultsSection = document.getElementById("results");
const resultsGrid = document.getElementById("results-grid");

// ── Slot management ────────────────────────────────────────────────────────

function createSlot(index) {
  const slot = document.createElement("div");
  slot.className = "product-slot";
  slot.dataset.index = index;

  slot.innerHTML = `
    <div class="slot-header">
      <span class="slot-number">Product ${index + 1}</span>
      ${index > 0 ? `<button class="btn-remove" type="button" aria-label="Remove product ${index + 1}">✕</button>` : ""}
    </div>
    <div class="form-group">
      <label for="name-${index}">Product Name <span class="required">*</span></label>
      <input type="text" id="name-${index}" class="product-name" placeholder="e.g. Magnetic Phone Mount" maxlength="100" required />
    </div>
    <div class="form-group">
      <label for="desc-${index}">Description <span class="required">*</span></label>
      <textarea id="desc-${index}" class="product-desc" placeholder="Describe the product, its use case, and target audience..." maxlength="500" rows="3" required></textarea>
    </div>
    <div class="form-group">
      <label for="img-${index}">Image URL <span class="optional">(optional)</span></label>
      <input type="url" id="img-${index}" class="product-img" placeholder="https://example.com/product.jpg" />
    </div>
  `;

  const removeBtn = slot.querySelector(".btn-remove");
  if (removeBtn) {
    removeBtn.addEventListener("click", () => removeSlot(slot));
  }

  return slot;
}

function addSlot() {
  if (slotCount >= MAX_SLOTS) return;
  const slot = createSlot(slotCount);
  slotsContainer.appendChild(slot);
  slotCount++;
  updateUI();
}

function removeSlot(slot) {
  slot.remove();
  slotCount--;
  // Re-number remaining slots
  const remaining = slotsContainer.querySelectorAll(".product-slot");
  remaining.forEach((s, i) => {
    s.dataset.index = i;
    s.querySelector(".slot-number").textContent = `Product ${i + 1}`;
    // Update input IDs
    s.querySelector(".product-name").id = `name-${i}`;
    s.querySelector(".product-desc").id = `desc-${i}`;
    s.querySelector(".product-img").id = `img-${i}`;
    // Show remove button on all except first
    const rb = s.querySelector(".btn-remove");
    if (i === 0 && rb) rb.remove();
  });
  updateUI();
}

function updateUI() {
  slotCounter.textContent = `${slotCount} / ${MAX_SLOTS}`;
  addBtn.disabled = slotCount >= MAX_SLOTS;
  addBtn.style.opacity = slotCount >= MAX_SLOTS ? "0.4" : "1";
}

// ── Form collection ────────────────────────────────────────────────────────

function collectProducts() {
  const slots = slotsContainer.querySelectorAll(".product-slot");
  const products = [];
  let valid = true;

  slots.forEach((slot) => {
    const name = slot.querySelector(".product-name").value.trim();
    const desc = slot.querySelector(".product-desc").value.trim();
    const img = slot.querySelector(".product-img").value.trim();

    // Clear previous errors
    slot.querySelectorAll(".field-error").forEach((e) => e.remove());
    slot.querySelectorAll(".input-error").forEach((el) => el.classList.remove("input-error"));

    if (!name) {
      markError(slot.querySelector(".product-name"), "Product name is required");
      valid = false;
    }
    if (!desc) {
      markError(slot.querySelector(".product-desc"), "Description is required");
      valid = false;
    }

    products.push({ name, description: desc, image_url: img || null });
  });

  return valid ? products : null;
}

function markError(input, message) {
  input.classList.add("input-error");
  const err = document.createElement("span");
  err.className = "field-error";
  err.textContent = message;
  input.parentNode.appendChild(err);
}

// ── Validate ───────────────────────────────────────────────────────────────

validateBtn.addEventListener("click", async () => {
  const products = collectProducts();
  if (!products) return;

  validateBtn.disabled = true;
  resultsSection.classList.add("hidden");
  showLoading(loadingEl);

  try {
    const res = await fetch(`${API_BASE}/validate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ products }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Unknown error" }));
      throw new Error(err.detail || `HTTP ${res.status}`);
    }

    const data = await res.json();
    renderResults(data.results);
  } catch (err) {
    showToast(`Analysis failed: ${err.message}`);
  } finally {
    hideLoading(loadingEl);
    validateBtn.disabled = false;
  }
});

// ── Render results ─────────────────────────────────────────────────────────

function renderResults(results) {
  resultsGrid.innerHTML = results.map((r) => buildResultCard(r)).join("");
  resultsSection.classList.remove("hidden");
  resultsSection.scrollIntoView({ behavior: "smooth" });
}

// ── Init ───────────────────────────────────────────────────────────────────

addBtn.addEventListener("click", addSlot);
addSlot(); // Start with one slot
