/**
 * Vocabulary Explorer View (Pure DOM Rendering)
 * =============================================
 */

class VocabView {
  constructor() {
    this.tableWrap = document.getElementById('index-table-wrap');
    this.countBadge = document.getElementById('vocab-count');
    this.filterInput = document.getElementById('vocab-filter');
    this.refreshBtn = document.getElementById('refresh-vocab-btn');
  }

  showLoading() {
    if (this.tableWrap) {
      this.tableWrap.innerHTML = `
        <div class="loading-state" style="padding:60px 20px;">
          <div class="spinner"></div>
          <h3>Loading index…</h3>
          <p>Reading vocabulary from positional index</p>
        </div>
      `;
    }
  }

  getFilterValue() {
    return this.filterInput ? this.filterInput.value.trim().toLowerCase() : '';
  }

  renderTable(termsList) {
    if (!this.tableWrap) return;
    if (!termsList || termsList.length === 0) {
      this.tableWrap.innerHTML = `
        <div class="empty-state" style="padding:40px;">
          <h3>No vocabulary terms matched</h3>
          <p>Try clearing your search filter.</p>
        </div>
      `;
      if (this.countBadge) this.countBadge.textContent = '0 terms';
      return;
    }

    if (this.countBadge) {
      this.countBadge.textContent = `${termsList.length} terms`;
    }

    const maxDf = Math.max(...termsList.map(t => t.df || 1), 1);

    let html = `
      <table class="ir-table">
        <thead>
          <tr>
            <th>Term</th>
            <th>Doc Freq (DF)</th>
            <th>IDF Weight</th>
            <th>Postings Preview (DocID &amp; TF)</th>
            <th>Sample Positions</th>
          </tr>
        </thead>
        <tbody>
    `;

    termsList.forEach(t => {
      const pct = Math.round((t.df / maxDf) * 100);
      const postingsHtml = (t.postings || t.postings_preview || []).map(p => {
        const dId = p.doc_id || (Array.isArray(p) ? p[0] : '');
        const tf = p.tf !== undefined ? p.tf : (Array.isArray(p) ? p[1] : 1);
        return `<span class="token-pill">${dId}<span class="pos-num">tf=${tf}</span></span>`;
      }).join('') + (t.has_more_postings ? '<span style="color:var(--text-muted);font-size:0.75rem;">…</span>' : '');

      const samplePosHtml = (t.sample_positions || []).map(pos => `<span class="token-pill" style="background:#EDE9FE;">[${pos}]</span>`).join('') || '<span style="color:var(--text-muted);font-size:0.75rem;">—</span>';

      html += `
        <tr>
          <td><strong style="font-family:var(--font-mono);font-size:0.88rem;">${t.term}</strong></td>
          <td>
            <div style="display:flex;align-items:center;gap:8px;">
              <span style="font-family:var(--font-mono);min-width:24px;">${t.df}</span>
              <div class="df-bar-bg" style="width:60px;height:6px;background:var(--border);border-radius:3px;overflow:hidden;">
                <div class="df-bar" style="width:${pct}%;height:100%;background:var(--purple);border-radius:3px;"></div>
              </div>
            </div>
          </td>
          <td><code style="font-size:0.82rem;">${t.idf}</code></td>
          <td><div class="token-grid">${postingsHtml}</div></td>
          <td><div class="token-grid">${samplePosHtml}</div></td>
        </tr>
      `;
    });

    html += `</tbody></table>`;
    this.tableWrap.innerHTML = html;
  }
}

window.VocabView = VocabView;
