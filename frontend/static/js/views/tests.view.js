/**
 * Tests View (Pure DOM Rendering)
 * ===============================
 */

class TestsView {
  constructor() {
    this.tableWrap = document.getElementById('test-table-wrap');
    this.refreshBtn = document.getElementById('refresh-tests-btn');
  }

  showLoading() {
    if (this.tableWrap) {
      this.tableWrap.innerHTML = `
        <div class="loading-state" style="padding:60px 20px;">
          <div class="spinner"></div>
          <h3>Running tests…</h3>
          <p>Executing all mandatory Part E queries on 100-garment corpus</p>
        </div>
      `;
    }
  }

  typePill(t) {
    const map = { vsm: 'type-vsm', exact_phrase: 'type-phrase', proximity: 'type-proximity', oov: 'type-oov' };
    const labels = { vsm: 'VSM', exact_phrase: 'Phrase', proximity: 'Proximity', oov: 'OOV' };
    return `<span class="type-pill ${map[t] || 'type-vsm'}">${labels[t] || t}</span>`;
  }

  renderTests(data, onRunQuery) {
    if (!this.tableWrap || !data) return;

    const allTests = [
      ...(data.free_text_tests || []).map(t => ({
        type: t.is_oov ? 'oov' : 'vsm',
        query: t.query,
        count: t.total_matches,
        top3: (t.top_docs || []).map(([id, sc]) => `${id} (${Number(sc).toFixed(3)})`).join(', ') || 'None (OOV)',
        evidence: t.is_oov ? 'No tokens in index vocabulary' : 'lnc.ltc cosine similarity'
      })),
      ...(data.exact_phrase_tests || []).map(t => ({
        type: 'exact_phrase',
        query: t.query,
        count: t.total_matches,
        top3: (t.matched_doc_ids || []).slice(0, 3).join(', ') || 'None',
        evidence: `pos(t2)=pos(t1)+1 · ${t.sample_positions ? JSON.stringify(t.sample_positions) : ''}`
      })),
      ...(data.proximity_tests || []).map(t => ({
        type: 'proximity',
        query: t.query,
        count: t.total_matches,
        top3: (t.matched_doc_ids || []).slice(0, 3).join(', ') || 'None',
        evidence: `0 < pos(t2)-pos(t1) <= ${t.k}`
      }))
    ];

    let html = `
      <table class="ir-table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Query</th>
            <th>Results</th>
            <th>Top-3 Document Matches</th>
            <th>Positional / Score Evidence</th>
          </tr>
        </thead>
        <tbody>
    `;

    allTests.forEach(t => {
      html += `
        <tr>
          <td>${this.typePill(t.type)}</td>
          <td>
            <a href="/results?q=${encodeURIComponent(t.query)}" class="test-query-link" style="color:var(--text-dark);font-weight:600;text-decoration:none;">
              ${t.query}
            </a>
          </td>
          <td><strong>${t.count}</strong></td>
          <td style="font-family:var(--font-mono);font-size:0.8rem;">${t.top3}</td>
          <td style="color:var(--text-muted);font-size:0.78rem;">${t.evidence}</td>
        </tr>
      `;
    });

    html += `</tbody></table>`;
    this.tableWrap.innerHTML = html;
  }
}

window.TestsView = TestsView;
