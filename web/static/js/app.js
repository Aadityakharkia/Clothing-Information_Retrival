/**
 * CLOTHING SEARCH ENGINE (CSD358 IR)
 * Frontend Application Logic
 * Clean Minimalist UI (Image 1) + Bold Sans Display (Image 2) + Crisp Clothing SVGs
 */

document.addEventListener("DOMContentLoaded", () => {
  initSearch();
  initNavTabs();
  initInnovations();
  initTracer();
  initBenchmark();
  initIndexExplorer();
  initModal();

  // Run initial search
  executeSearch("breathable cotton t-shirt");
});

// State
let currentQuery = "";
let selectedRelevantDocs = new Set();
let isProximityBoostActive = false;

// Garment SVG Icons Map (Hand-crafted Clean Vectors, Zero AI Artifacts)
const CLOTHING_ICONS = {
  "T-Shirt": `<svg class="clothing-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"></path></svg>`,
  "Shirt": `<svg class="clothing-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 4 16 2a4 4 0 0 1-8 0L4 4l-2 6 4 2V22h12V12l4-2-2-6z"></path><path d="M12 2v20"></path><circle cx="12" cy="7" r="0.5" fill="currentColor"></circle><circle cx="12" cy="11" r="0.5" fill="currentColor"></circle><circle cx="12" cy="15" r="0.5" fill="currentColor"></circle></svg>`,
  "Jeans": `<svg class="clothing-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 2h16v3l-2 17h-5l-1-11-1 11H6L4 5V2z"></path><path d="M4 6h16"></path><path d="M12 2v6"></path></svg>`,
  "Kurta": `<svg class="clothing-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 2 8 2l-4 4 3 3v13h10V9l3-3-4-4z"></path><path d="M12 2v7"></path><path d="M10 9h4"></path></svg>`,
  "Saree": `<svg class="clothing-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a8 8 0 0 0-8 8c0 5 8 12 8 12s8-7 8-12a8 8 0 0 0-8-8z"></path><circle cx="12" cy="10" r="3"></circle></svg>`,
  "Dress": `<svg class="clothing-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 2h6l2 5-3 15H10L7 7l2-5z"></path><path d="M9 7h6"></path></svg>`,
  "Hoodie": `<svg class="clothing-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a5 5 0 0 0-5 5v1L2 11l3 3 1-1v8h12v-8l1 1 3-3-5-3V7a5 5 0 0 0-5-5z"></path><path d="M9 14h6"></path></svg>`,
  "Jacket": `<svg class="clothing-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16l2 8-5 1v9H7v-9L2 12l2-8z"></path><path d="M12 4v18"></path></svg>`,
  "Leggings": `<svg class="clothing-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 2h14v2l-2 18h-4l-1-10-1 10H7L5 4V2z"></path></svg>`,
  "Sweatshirt": `<svg class="clothing-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 4 15 2H9L5 4 2 9l3 2v11h14V11l3-2-3-5z"></path><path d="M9 2a3 3 0 0 0 6 0"></path></svg>`
};

function getClothingIcon(category) {
  return CLOTHING_ICONS[category] || CLOTHING_ICONS["T-Shirt"];
}

// =============================================================================
// Search Dispatcher & Event Bindings
// =============================================================================
function initSearch() {
  const searchInput = document.getElementById("main-search-input");
  const searchBtn = document.getElementById("main-search-btn");

  searchBtn.addEventListener("click", () => {
    executeSearch(searchInput.value.trim());
  });

  searchInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      executeSearch(searchInput.value.trim());
    }
  });

  // Query chips
  document.querySelectorAll(".q-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const q = chip.getAttribute("data-q");
      searchInput.value = q;
      executeSearch(q);
    });
  });
}

// =============================================================================
// Navigation Tabs
// =============================================================================
function initNavTabs() {
  const tabBtns = document.querySelectorAll(".menu-item");
  const heroSection = document.getElementById("hero-section");
  const resultsSection = document.getElementById("results-stream-section");
  const tracerSection = document.getElementById("tracer-tab-panel");
  const benchmarkSection = document.getElementById("benchmark-tab-panel");
  const indexSection = document.getElementById("index-tab-panel");

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const target = btn.getAttribute("data-tab");

      tabBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      // Hide all tabs
      heroSection.style.display = "none";
      resultsSection.style.display = "none";
      tracerSection.style.display = "none";
      benchmarkSection.style.display = "none";
      indexSection.style.display = "none";

      if (target === "search-view") {
        heroSection.style.display = "block";
        resultsSection.style.display = "block";
      } else if (target === "tracer-view") {
        tracerSection.style.display = "block";
      } else if (target === "benchmark-view") {
        benchmarkSection.style.display = "block";
        loadBenchmark();
      } else if (target === "index-view") {
        indexSection.style.display = "block";
        loadIndex();
      }
    });
  });

  document.getElementById("nav-brand-logo").addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("tab-search-btn").click();
  });
}

// =============================================================================
// Search Execution: VSM or Positional
// =============================================================================
async function executeSearch(query) {
  if (!query) return;
  currentQuery = query;
  selectedRelevantDocs.clear();
  updateRocchioBtn();

  const grid = document.getElementById("garments-grid");
  const countText = document.getElementById("results-count-text");
  const queryEcho = document.getElementById("results-query-echo");
  const modeBadge = document.getElementById("results-mode-badge");

  grid.innerHTML = `<div style="padding: 40px; color: var(--text-muted);">Searching clothing corpus...</div>`;
  queryEcho.textContent = `for "${query}"`;

  const isPositional = query.startsWith('"') || query.includes("WITHIN/");

  if (isPositional) {
    modeBadge.textContent = "Positional Index";
    await searchPositional(query);
  } else {
    modeBadge.textContent = isProximityBoostActive ? "Hybrid Proximity Boost (lnc.ltc)" : "VSM Ranked (lnc.ltc)";
    await searchVSM(query);
  }
}

async function searchVSM(query) {
  const endpoint = isProximityBoostActive
    ? `/api/search/hybrid?q=${encodeURIComponent(query)}&lambda=0.5&top_k=10`
    : `/api/search/vsm?q=${encodeURIComponent(query)}&top_k=10`;

  try {
    const res = await fetch(endpoint);
    const data = await res.json();
    renderVSMResults(data);
  } catch (err) {
    document.getElementById("garments-grid").innerHTML = `<div style="color: red; padding: 20px;">Error: ${err.message}</div>`;
  }
}

async function searchPositional(query) {
  try {
    const res = await fetch(`/api/search/positional?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    renderPositionalResults(data);
  } catch (err) {
    document.getElementById("garments-grid").innerHTML = `<div style="color: red; padding: 20px;">Error: ${err.message}</div>`;
  }
}

// =============================================================================
// Render VSM Results & Update Image 1 Showcase Card
// =============================================================================
function renderVSMResults(data) {
  const grid = document.getElementById("garments-grid");
  const countText = document.getElementById("results-count-text");

  countText.textContent = `Top ${data.results.length} Ranked Garments`;

  if (data.results.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1 / -1; padding: 50px 20px; text-align: center;">
        <h3 style="font-family: var(--font-display); font-size: 1.4rem; margin-bottom: 8px;">No garments matched</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem;">
          Query terms are out-of-vocabulary or not found in the 100-document clothing corpus.
        </p>
      </div>
    `;
    return;
  }

  // Update Right Showcase Card with Top Match #1
  const top1 = data.results[0];
  updateShowcaseCard(top1, "vsm");

  const queryTerms = (data.query || "").toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/).filter(w => w.length > 2);

  grid.innerHTML = data.results.map((item, idx) => {
    const score = item.hybrid_score !== undefined ? item.hybrid_score : item.cosine_score;
    const highlightedSnippet = highlightSnippet(item.text, queryTerms);
    const iconSvg = getClothingIcon(item.category);

    return `
      <div class="garment-card">
        <div>
          <div class="card-meta-top">
            <span class="rank-pill">#${item.rank}</span>
            <div style="display: flex; align-items: center; gap: 6px;">
              ${iconSvg}
              <span class="cat-pill">${escapeHtml(item.category)}</span>
            </div>
            <span class="id-pill">${item.doc_id}</span>
          </div>

          <h3 class="garment-title" onclick="openDocModal('${item.doc_id}')">${escapeHtml(item.title)}</h3>
          <p class="garment-snippet">${highlightedSnippet}</p>
        </div>

        <div>
          <div class="card-score-strip">
            <span class="score-lbl">${item.hybrid_score !== undefined ? "Hybrid Score:" : "Cosine Score (lnc.ltc):"}</span>
            <span class="score-val">${score.toFixed(6)}</span>
          </div>

          ${item.shortest_span ? `
            <div class="evidence-badge-strip">
              Shortest Span: ${item.shortest_span} tokens &bull; Boost: &times;${item.boost_factor.toFixed(2)}
            </div>
          ` : ''}

          <div class="card-footer-row">
            <label class="rel-label">
              <input type="checkbox" class="rel-box" data-id="${item.doc_id}">
              <span>Relevant</span>
            </label>
            <button class="inspect-link" onclick="openDocModal('${item.doc_id}')">
              <span>Inspect details</span> &rarr;
            </button>
          </div>
        </div>
      </div>
    `;
  }).join("");

  // Attach relevance checkboxes
  document.querySelectorAll(".rel-box").forEach(box => {
    box.addEventListener("change", () => {
      const id = box.getAttribute("data-id");
      if (box.checked) selectedRelevantDocs.add(id);
      else selectedRelevantDocs.delete(id);
      updateRocchioBtn();
    });
  });
}

// =============================================================================
// Render Positional Results
// =============================================================================
function renderPositionalResults(data) {
  const grid = document.getElementById("garments-grid");
  const countText = document.getElementById("results-count-text");

  countText.textContent = `${data.total_matches} Exact Positional Matches`;

  if (data.results.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1 / -1; padding: 50px 20px; text-align: center;">
        <h3 style="font-family: var(--font-display); font-size: 1.4rem; margin-bottom: 8px;">No exact positional matches</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem;">
          Terms did not appear in consecutive order or within the requested token distance.
        </p>
      </div>
    `;
    return;
  }

  // Update Right Showcase Card with Top Positional Match
  const top1 = data.results[0];
  updateShowcaseCard(top1, "positional");

  const queryTerms = data.results[0].query_terms || [];

  grid.innerHTML = data.results.map((item, idx) => {
    const highlightedSnippet = highlightSnippet(item.text, queryTerms);
    const iconSvg = getClothingIcon(item.category);

    let evidenceHtml = "";
    if (item.matched_positions) {
      evidenceHtml = `
        <div class="evidence-badge-strip">
          ✓ Exact Match Positions: ${JSON.stringify(item.matched_positions)}
        </div>
      `;
    } else if (item.matched_pairs) {
      const pairs = item.matched_pairs.map(p => `(${p[0]}, ${p[1]}, dist=${p[2]})`).join(", ");
      evidenceHtml = `
        <div class="evidence-badge-strip">
          ✓ Proximity Pairs: [${pairs}]
        </div>
      `;
    }

    return `
      <div class="garment-card">
        <div>
          <div class="card-meta-top">
            <span class="rank-pill">#${idx + 1}</span>
            <div style="display: flex; align-items: center; gap: 6px;">
              ${iconSvg}
              <span class="cat-pill">${escapeHtml(item.category)}</span>
            </div>
            <span class="id-pill">${item.doc_id}</span>
          </div>

          <h3 class="garment-title" onclick="openDocModal('${item.doc_id}')">${escapeHtml(item.title)}</h3>
          <p class="garment-snippet">${highlightedSnippet}</p>
        </div>

        <div>
          ${evidenceHtml}

          <div class="card-footer-row">
            <span style="font-size: 0.74rem; font-weight: 700; color: #7928ca;">Positional Index Verified</span>
            <button class="inspect-link" onclick="openDocModal('${item.doc_id}')">
              <span>Inspect details</span> &rarr;
            </button>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

// =============================================================================
// Update Showcase Card (Image 1 Style)
// =============================================================================
function updateShowcaseCard(item, mode) {
  document.getElementById("card-doc-id").textContent = item.doc_id;
  document.getElementById("card-title").textContent = item.title;

  const specsBox = document.getElementById("card-specs");
  specsBox.innerHTML = `
    <div class="spec-row"><span class="spec-bullet">&bull;</span><span>Category: <strong>${escapeHtml(item.category)}</strong></span></div>
    <div class="spec-row"><span class="spec-bullet">&bull;</span><span>Product ID: <strong>${item.doc_id}</strong></span></div>
    <div class="spec-row"><span class="spec-bullet">&bull;</span><span>Length Norm: <strong>${item.vector_length || '2.828'}</strong></span></div>
  `;

  if (mode === "vsm") {
    const score = item.hybrid_score !== undefined ? item.hybrid_score : item.cosine_score;
    document.getElementById("card-rank").textContent = `Rank #${item.rank || 1}`;
    document.getElementById("card-score").textContent = `Score: ${score.toFixed(4)}`;
    document.getElementById("card-phrase-tag").textContent = item.shortest_span ? `Span Boost: ${item.shortest_span} tokens` : "Ranked via lnc.ltc Cosine Score";
  } else {
    document.getElementById("card-rank").textContent = "Positional Match";
    document.getElementById("card-score").textContent = `${item.match_count || 1} Occurrence(s)`;
    document.getElementById("card-phrase-tag").textContent = item.matched_positions ? `Positions: ${JSON.stringify(item.matched_positions[0])}` : "Ordered WITHIN/k Verified";
  }
}

// =============================================================================
// Special Ideas 1 (Hybrid Boost) & 3 (Rocchio)
// =============================================================================
function initInnovations() {
  const boostToggle = document.getElementById("toggle-proximity-boost");
  const prfBtn = document.getElementById("btn-prf");
  const rocchioBtn = document.getElementById("btn-rocchio");
  const resetBtn = document.getElementById("btn-reset-rocchio");

  boostToggle.addEventListener("change", () => {
    isProximityBoostActive = boostToggle.checked;
    if (currentQuery) executeSearch(currentQuery);
  });

  prfBtn.addEventListener("click", () => {
    if (!currentQuery) return;
    runRocchio({ query: currentQuery, is_prf: true });
  });

  rocchioBtn.addEventListener("click", () => {
    if (!currentQuery || selectedRelevantDocs.size === 0) return;
    runRocchio({
      query: currentQuery,
      relevant_doc_ids: Array.from(selectedRelevantDocs),
      is_prf: false
    });
  });

  resetBtn.addEventListener("click", () => {
    resetBtn.style.display = "none";
    document.getElementById("rocchio-exp-strip").style.display = "none";
    selectedRelevantDocs.clear();
    updateRocchioBtn();
    executeSearch(currentQuery);
  });
}

function updateRocchioBtn() {
  const btn = document.getElementById("btn-rocchio");
  const countSpan = document.getElementById("rocchio-selected-count");
  const count = selectedRelevantDocs.size;
  countSpan.textContent = count;
  btn.disabled = count === 0;
}

async function runRocchio(payload) {
  const expStrip = document.getElementById("rocchio-exp-strip");
  const expPills = document.getElementById("rocchio-exp-pills");
  const resetBtn = document.getElementById("btn-reset-rocchio");

  try {
    const res = await fetch("/api/rocchio", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    if (data.top_expanded_terms && data.top_expanded_terms.length > 0) {
      expStrip.style.display = "flex";
      expPills.innerHTML = data.top_expanded_terms.map(t =>
        `<span class="exp-pill">${t.term} (+${t.gain.toFixed(3)})</span>`
      ).join("");
      resetBtn.style.display = "inline-block";
    }

    renderRocchioResults(data);
  } catch (err) {
    alert("Rocchio Error: " + err.message);
  }
}

function renderRocchioResults(data) {
  const grid = document.getElementById("garments-grid");
  const countText = document.getElementById("results-count-text");

  countText.textContent = `Top ${data.results.length} Garments (Rocchio Re-ranked)`;

  if (data.results.length > 0) {
    updateShowcaseCard(data.results[0], "vsm");
  }

  grid.innerHTML = data.results.map((item) => {
    const iconSvg = getClothingIcon(item.category);
    return `
      <div class="garment-card" style="${item.is_marked_relevant ? 'border-color: #a855f7;' : ''}">
        <div>
          <div class="card-meta-top">
            <span class="rank-pill">#${item.rank}</span>
            <div style="display: flex; align-items: center; gap: 6px;">
              ${iconSvg}
              <span class="cat-pill">${escapeHtml(item.category)}</span>
            </div>
            <span class="id-pill">${item.doc_id}</span>
          </div>

          <h3 class="garment-title" onclick="openDocModal('${item.doc_id}')">${escapeHtml(item.title)}</h3>
          <p class="garment-snippet">${escapeHtml(item.text)}</p>
        </div>

        <div>
          <div class="card-score-strip">
            <span class="score-lbl">Rocchio Mod Score:</span>
            <span class="score-val">${item.rocchio_score.toFixed(6)}</span>
          </div>

          <div class="card-footer-row">
            <span style="font-size: 0.74rem; font-weight: 700; color: ${item.is_marked_relevant ? '#7928ca' : '#737373'};">
              ${item.is_marked_relevant ? '★ Feedback Seed' : 'Re-ranked Candidate'}
            </span>
            <button class="inspect-link" onclick="openDocModal('${item.doc_id}')">
              <span>Inspect details</span> &rarr;
            </button>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

// =============================================================================
// Special Idea 2: Positional Intersection Tracer
// =============================================================================
function initTracer() {
  const btn = document.getElementById("trace-execute-btn");
  const t1 = document.getElementById("trace-t1");
  const t2 = document.getElementById("trace-t2");
  const k = document.getElementById("trace-k");

  btn.addEventListener("click", () => {
    executeTracer(t1.value.trim(), t2.value.trim(), k.value);
  });

  document.querySelectorAll(".preset-pill").forEach(pill => {
    pill.addEventListener("click", () => {
      t1.value = pill.getAttribute("data-t1");
      t2.value = pill.getAttribute("data-t2");
      k.value = pill.getAttribute("data-k");
      executeTracer(t1.value, t2.value, k.value);
    });
  });
}

async function executeTracer(term1, term2, dist) {
  const logBox = document.getElementById("trace-log-box");
  const matchesBox = document.getElementById("trace-matches-box");
  const countBadge = document.getElementById("trace-matches-count");

  logBox.innerHTML = `<em>Intersecting '${term1}' and '${term2}' (k=${dist})...</em>`;
  matchesBox.innerHTML = ``;

  try {
    const res = await fetch(`/api/trace?term1=${encodeURIComponent(term1)}&term2=${encodeURIComponent(term2)}&k=${dist}`);
    const data = await res.json();

    countBadge.textContent = `Matches: ${data.total_matches}`;

    logBox.innerHTML = data.trace_log.map(line => {
      let cls = "log-entry";
      if (line.includes("Valid proximity")) cls += " valid";
      else if (line.includes("Doc match found")) cls += " match";
      else if (line.includes("Advancing")) cls += " step";
      return `<div class="${cls}">${escapeHtml(line)}</div>`;
    }).join("");

    if (data.matches.length === 0) {
      matchesBox.innerHTML = `<div style="padding: 16px; color: var(--text-muted);">No garments fulfilled the proximity distance &le; ${dist}.</div>`;
    } else {
      matchesBox.innerHTML = data.matches.map(m => `
        <div class="match-item-card">
          <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <strong style="color: #7928ca;">${m.doc_id}</strong>
            <span style="font-size: 0.72rem; color: var(--text-muted);">${m.category}</span>
          </div>
          <div style="font-size: 0.85rem; font-weight: 700; margin-bottom: 6px;">${m.title}</div>
          <div style="font-size: 0.74rem; font-family: var(--font-mono); color: #065f46;">
            Pairs: ${m.matched_pairs.map(p => `(${p[0]}, ${p[1]}, d=${p[2]})`).join(", ")}
          </div>
        </div>
      `).join("");
    }
  } catch (err) {
    logBox.innerHTML = `<div style="color: red;">Error: ${err.message}</div>`;
  }
}

// =============================================================================
// Benchmark & Test Suite (Part E)
// =============================================================================
let benchmarkLoaded = false;

async function loadBenchmark() {
  if (benchmarkLoaded) return;
  const container = document.getElementById("benchmark-tables-box");
  container.innerHTML = `<div style="padding: 30px; color: var(--text-muted);">Running test suite...</div>`;

  try {
    const res = await fetch("/api/tests");
    const data = await res.json();
    renderBenchmarkTables(data);
    benchmarkLoaded = true;
  } catch (err) {
    container.innerHTML = `<div style="color: red; padding: 20px;">Error: ${err.message}</div>`;
  }
}

function renderBenchmarkTables(data) {
  const container = document.getElementById("benchmark-tables-box");

  let html = `
    <h3 style="font-family: var(--font-display); font-size: 1.3rem; margin: 24px 0 12px; font-weight: 900;">1. Free-Text Ranked Tests (VSM lnc.ltc &bull; 10 Queries)</h3>
    ${data.free_text_tests.map((test, idx) => `
      <div style="margin-bottom: 22px;">
        <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 6px;">
          Query ${idx + 1}: <code style="color: #7928ca;">${escapeHtml(test.query)}</code>
          ${test.query.includes("cyberpunk") ? '<span style="font-size: 0.7rem; background: #ffe4e6; color: #be123c; padding: 2px 6px; border-radius: 4px; margin-left: 6px;">Out-Of-Vocabulary</span>' : ''}
        </h4>
        <div class="table-card">
          <table class="minimal-table">
            <thead>
              <tr>
                <th style="width: 50px;">Rank</th>
                <th style="width: 80px;">DocID</th>
                <th style="width: 110px;">Category</th>
                <th>Title</th>
                <th style="width: 120px;">Cosine Score</th>
              </tr>
            </thead>
            <tbody>
              ${test.top_10_results.length === 0 ? `
                <tr><td colspan="5" style="text-align: center; color: var(--text-muted);">*No matches (Out-Of-Vocabulary terms)*</td></tr>
              ` : test.top_10_results.map(r => `
                <tr>
                  <td><strong>#${r.rank}</strong></td>
                  <td><code>${r.doc_id}</code></td>
                  <td>${r.category}</td>
                  <td>${r.title}</td>
                  <td style="font-family: var(--font-mono); font-weight: 700; color: #111827;">${r.cosine_score.toFixed(6)}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
    `).join("")}

    <h3 style="font-family: var(--font-display); font-size: 1.3rem; margin: 32px 0 12px; font-weight: 900;">2. Exact Phrase Queries (Positional Index &bull; 5 Queries)</h3>
    ${data.exact_phrase_tests.map((test, idx) => `
      <div style="margin-bottom: 22px;">
        <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 6px;">
          Phrase Query ${idx + 1}: <code style="color: #7928ca;">${escapeHtml(test.query)}</code>
          <span style="font-size: 0.78rem; color: var(--text-muted); font-weight: 400;">(${test.total_matches} matches)</span>
        </h4>
        <div class="table-card">
          <table class="minimal-table">
            <thead>
              <tr>
                <th style="width: 80px;">DocID</th>
                <th style="width: 110px;">Category</th>
                <th>Title</th>
                <th style="width: 70px;">Matches</th>
                <th>Matched Token Positions [p1, p2, ...]</th>
              </tr>
            </thead>
            <tbody>
              ${test.results.map(r => `
                <tr>
                  <td><code>${r.doc_id}</code></td>
                  <td>${r.category}</td>
                  <td>${r.title}</td>
                  <td>${r.match_count}</td>
                  <td style="font-family: var(--font-mono); color: #7928ca;">${JSON.stringify(r.matched_positions)}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
    `).join("")}

    <h3 style="font-family: var(--font-display); font-size: 1.3rem; margin: 32px 0 12px; font-weight: 900;">3. Proximity Queries (Positional Index &bull; WITHIN/k)</h3>
    ${data.proximity_tests.map((test, idx) => `
      <div style="margin-bottom: 22px;">
        <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 6px;">
          Proximity Query ${idx + 1}: <code style="color: #7928ca;">${escapeHtml(test.query)}</code>
          <span style="font-size: 0.78rem; color: var(--text-muted); font-weight: 400;">(k=${test.k}, ${test.total_matches} matches)</span>
        </h4>
        <div class="table-card">
          <table class="minimal-table">
            <thead>
              <tr>
                <th style="width: 80px;">DocID</th>
                <th style="width: 110px;">Category</th>
                <th>Title</th>
                <th style="width: 70px;">Matches</th>
                <th>Position Pairs (pos1, pos2, dist)</th>
              </tr>
            </thead>
            <tbody>
              ${test.results.map(r => `
                <tr>
                  <td><code>${r.doc_id}</code></td>
                  <td>${r.category}</td>
                  <td>${r.title}</td>
                  <td>${r.match_count}</td>
                  <td style="font-family: var(--font-mono); color: #7928ca;">
                    ${r.matched_pairs.map(p => `(${p[0]}, ${p[1]}, d=${p[2]})`).join(", ")}
                  </td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        </div>
      </div>
    `).join("")}
  `;

  container.innerHTML = html;
}

function initBenchmark() {
  document.getElementById("btn-refresh-suite").addEventListener("click", () => {
    benchmarkLoaded = false;
    loadBenchmark();
  });
}

// =============================================================================
// Vocabulary & Index Explorer
// =============================================================================
let indexLoaded = false;
let allIndexTerms = [];

async function loadIndex() {
  if (indexLoaded) return;
  const tbody = document.getElementById("index-tbody");
  tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">Loading vocabulary...</td></tr>`;

  try {
    const res = await fetch("/output/positional_index.json");
    const posIndex = await res.json();

    allIndexTerms = Object.keys(posIndex).map(term => ({
      term,
      df: posIndex[term].df,
      idf: (Math.log10(100 / posIndex[term].df)).toFixed(4),
      postings: posIndex[term].postings
    }));

    renderIndexRows(allIndexTerms);
    indexLoaded = true;
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="4" style="color: red;">Error: ${err.message}</td></tr>`;
  }
}

function renderIndexRows(terms) {
  const tbody = document.getElementById("index-tbody");
  tbody.innerHTML = terms.map(item => {
    const sample = item.postings.slice(0, 4).map(p =>
      `${p[0]}[tf=${p[1]}: ${JSON.stringify(p[2])}]`
    ).join("; ");
    const more = item.postings.length > 4 ? ` ... (+${item.postings.length - 4} docs)` : "";

    return `
      <tr>
        <td><strong style="color: #7928ca;">${escapeHtml(item.term)}</strong></td>
        <td><code>${item.df}</code></td>
        <td><code>${item.idf}</code></td>
        <td style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-body);">${sample}${more}</td>
      </tr>
    `;
  }).join("");
}

function initIndexExplorer() {
  const filterInput = document.getElementById("index-filter-input");
  filterInput.addEventListener("input", () => {
    const q = filterInput.value.trim().toLowerCase();
    const filtered = allIndexTerms.filter(t => t.term.toLowerCase().includes(q));
    renderIndexRows(filtered);
  });
}

// =============================================================================
// Document Inspection Modal
// =============================================================================
function initModal() {
  const modal = document.getElementById("doc-modal");
  const closeBtn = document.getElementById("modal-close");

  closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  window.addEventListener("click", (e) => {
    if (e.target === modal) modal.style.display = "none";
  });
}

async function openDocModal(docId) {
  const modal = document.getElementById("doc-modal");
  const mTitle = document.getElementById("modal-title");
  const mDocId = document.getElementById("modal-doc-id");
  const mContent = document.getElementById("modal-content");

  modal.style.display = "flex";
  mDocId.textContent = docId;
  mTitle.textContent = "Loading Garment Document...";
  mContent.innerHTML = `<div style="text-align: center; padding: 20px;">Fetching document...</div>`;

  try {
    const res = await fetch(`/api/doc/${docId}`);
    const doc = await res.json();

    mTitle.textContent = doc.title;
    mContent.innerHTML = `
      <div style="margin-bottom: 14px;">
        <span style="font-size: 0.78rem; font-weight: 800; text-transform: uppercase; color: #7928ca;">${doc.category}</span>
        <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 4px;">
          Vector Euclidean Norm: <strong>${doc.vector_length}</strong> &bull; Non-Stop Terms: <strong>${doc.tokens.length}</strong>
        </div>
      </div>

      <div style="background: var(--bg-subtle); border: 1px solid var(--border-light); border-radius: var(--radius-sm); padding: 14px; margin-bottom: 18px; font-size: 0.9rem; line-height: 1.6;">
        ${escapeHtml(doc.text)}
      </div>

      <h4 style="font-size: 0.8rem; font-weight: 800; text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px;">Tokenized Sequence &amp; Positional Offsets [pos]</h4>
      <div style="display: flex; flex-wrap: wrap; gap: 5px; max-height: 220px; overflow-y: auto;">
        ${doc.tokens.map(t => `
          <span style="font-family: var(--font-mono); font-size: 0.74rem; background: #ffffff; border: 1px solid var(--border-light); padding: 2px 6px; border-radius: 4px;">
            ${t.term}<sup style="color: #7928ca; font-weight: 700;">[${t.pos}]</sup>
          </span>
        `).join("")}
      </div>
    `;
  } catch (err) {
    mContent.innerHTML = `<div style="color: red;">Error: ${err.message}</div>`;
  }
}

// =============================================================================
// Helper Utilities
// =============================================================================
function highlightSnippet(text, queryWords) {
  if (!queryWords || queryWords.length === 0) return escapeHtml(text);
  let escaped = escapeHtml(text);

  queryWords.forEach(w => {
    if (w.length > 2) {
      const regex = new RegExp(`\\b(${w}[a-z]*)\\b`, "gi");
      escaped = escaped.replace(regex, `<mark>$1</mark>`);
    }
  });

  return escaped;
}

function escapeHtml(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
