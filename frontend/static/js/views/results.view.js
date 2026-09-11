/**
 * Results View (Pure DOM Rendering)
 * =================================
 * Deterministic DOM updates for ranked results, badges, metrics, and cards.
 */

class ResultsView {
  constructor() {
    this.listContainer = document.getElementById('results-list');
    this.countLabel = document.getElementById('results-count-label');
    this.modeBadge = document.getElementById('results-mode-badge');
    this.qDisplay = document.getElementById('q-display');
    this.selectedCountLabel = document.getElementById('sel-count');
    this.rocchioBtn = document.getElementById('rocchio-btn');
    this.resetBtn = document.getElementById('reset-btn');
    this.expTermsWrap = document.getElementById('exp-terms-wrap');
    this.expTermsList = document.getElementById('exp-terms-list');
  }

  showLoading() {
    if (this.listContainer) {
      this.listContainer.innerHTML = `
        <div class="loading-state">
          <div class="spinner"></div>
          <p>Retrieving documents from inverted index…</p>
        </div>
      `;
    }
  }

  showEmpty(query) {
    if (this.listContainer) {
      this.listContainer.innerHTML = `
        <div class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <h3>No matching garments found</h3>
          <p>Try broadening your terms or removing specific constraints.</p>
        </div>
      `;
    }
    if (this.countLabel) this.countLabel.textContent = '0 results';
  }

  renderResults(results, mode, query, onToggleDoc, onOpenDoc) {
    if (!this.listContainer) return;
    if (!results || results.length === 0) {
      this.showEmpty(query);
      return;
    }

    if (this.countLabel) {
      this.countLabel.textContent = `${results.length} garment${results.length === 1 ? '' : 's'} found`;
    }

    let html = '';
    results.forEach((item, idx) => {
      const rank = item.rank || (idx + 1);
      const isVSM = mode === 'vsm' || mode === 'hybrid';
      const scoreDisplay = isVSM 
        ? (item.hybrid_score !== undefined ? `Hybrid: ${item.hybrid_score}` : `Cosine: ${item.cosine_score || 0}`)
        : (item.match_count ? `${item.match_count} match${item.match_count === 1 ? '' : 'es'}` : 'Matched');

      const isBoosted = item.boost_factor && item.boost_factor > 1.0;
      const boostBadge = isBoosted 
        ? `<span class="score-pill score-boost" title="Span: ${item.shortest_span}">▲ +${Math.round((item.boost_factor - 1) * 100)}% Boost</span>`
        : '';

      const termChips = Object.entries(item.term_contributions || {})
        .slice(0, 5)
        .map(([t, c]) => `<span class="contrib-chip">${t}: +${Number(c).toFixed(3)}</span>`)
        .join('');

      html += `
        <article class="result-card" data-doc-id="${item.doc_id}" id="card-${item.doc_id}">
          <div class="rc-head">
            <div class="rc-badges">
              <span class="rank-badge">#${rank}</span>
              <span class="docid-badge">${item.doc_id}</span>
              <span class="cat-badge">${item.category || 'Apparel'}</span>
            </div>
            <div class="rc-actions">
              ${boostBadge}
              <span class="score-pill ${isVSM ? 'score-vsm' : 'score-pos'}">${scoreDisplay}</span>
              <button class="inspect-btn" data-doc-id="${item.doc_id}" title="Inspect Document Vectors & Postings">
                Inspect
              </button>
            </div>
          </div>
          <h2 class="rc-title">${item.title}</h2>
          <p class="rc-desc">${(item.text || '').substring(0, 240)}…</p>
          ${termChips ? `<div class="rc-terms">${termChips}</div>` : ''}
          ${mode === 'vsm' ? `
            <div class="rc-foot">
              <label class="fb-checkbox-label">
                <input type="checkbox" class="rel-doc-checkbox" data-doc-id="${item.doc_id}">
                <span>Mark Relevant for Rocchio Feedback</span>
              </label>
            </div>
          ` : ''}
        </article>
      `;
    });

    this.listContainer.innerHTML = html;

    // Attach listeners
    this.listContainer.querySelectorAll('.inspect-btn').forEach(btn => {
      btn.addEventListener('click', () => onOpenDoc(btn.dataset.docId));
    });

    if (onToggleDoc) {
      this.listContainer.querySelectorAll('.rel-doc-checkbox').forEach(chk => {
        chk.addEventListener('change', () => onToggleDoc(chk.dataset.docId, chk.checked));
      });
    }
  }

  updateSelectionCount(count) {
    if (this.selectedCountLabel) this.selectedCountLabel.textContent = count;
    if (this.rocchioBtn) this.rocchioBtn.disabled = count === 0;
  }

  renderExpandedTerms(expansions) {
    if (!this.expTermsWrap || !this.expTermsList) return;
    if (!expansions || expansions.length === 0) {
      this.expTermsWrap.style.display = 'none';
      return;
    }
    this.expTermsWrap.style.display = 'block';
    if (this.resetBtn) this.resetBtn.style.display = 'block';
    this.expTermsList.innerHTML = expansions.map(e => `
      <span class="token-pill">
        ${e.term} <span class="pos-num">+${e.gain}</span>
      </span>
    `).join('');
  }
}

window.ResultsView = ResultsView;
