/**
 * Tracer View (Pure DOM Rendering)
 * ================================
 */

class TracerView {
  constructor() {
    this.t1Input = document.getElementById('trace-t1');
    this.t2Input = document.getElementById('trace-t2');
    this.kInput = document.getElementById('trace-k');
    this.traceBtn = document.getElementById('trace-btn');
    this.matchCountBadge = document.getElementById('trace-match-count');
    this.terminalBody = document.getElementById('trace-log');
    this.matchesBody = document.getElementById('trace-matches');
  }

  getInputs() {
    return {
      term1: this.t1Input ? this.t1Input.value.trim() : '',
      term2: this.t2Input ? this.t2Input.value.trim() : '',
      k: this.kInput ? parseInt(this.kInput.value, 10) || 4 : 4
    };
  }

  setInputs(term1, term2, k) {
    if (this.t1Input) this.t1Input.value = term1;
    if (this.t2Input) this.t2Input.value = term2;
    if (this.kInput) this.kInput.value = k;
  }

  showLoading() {
    if (this.terminalBody) {
      this.terminalBody.innerHTML = '<span class="log-info">Simulating Positional Intersect merge…</span>';
    }
    if (this.matchesBody) {
      this.matchesBody.innerHTML = '<p class="placeholder-hint">Tracing matching documents…</p>';
    }
  }

  renderTraceResults(data, onOpenDoc) {
    if (!data) return;

    if (this.matchCountBadge) {
      this.matchCountBadge.textContent = `Matches: ${data.total_matches || (data.matches ? data.matches.length : 0)}`;
    }

    // Render Terminal Log
    if (this.terminalBody) {
      const logs = data.trace_log || [];
      this.terminalBody.innerHTML = logs.map(line => {
        let cls = 'log-line';
        if (line.includes('accepted')) cls = 'log-ok';
        else if (line.includes('rejected')) cls = 'log-warn';
        else if (line.startsWith('Starting') || line.startsWith('Postings')) cls = 'log-info';
        return `<span class="${cls}">${line}</span>`;
      }).join('');
    }

    // Render Matches
    if (this.matchesBody) {
      const matches = data.matches || [];
      if (matches.length === 0) {
        this.matchesBody.innerHTML = '<p class="placeholder-hint">No document pairs satisfied the proximity condition within distance k.</p>';
        return;
      }

      this.matchesBody.innerHTML = matches.map(m => {
        const pairsHtml = (m.matched_pairs || []).map(([p1, p2, dist]) => `
          <span class="token-pill">
            pos(${data.term1})=${p1} → pos(${data.term2})=${p2}
            <span class="pos-num">dist=${dist}</span>
          </span>
        `).join('');

        return `
          <div class="result-card" style="margin-bottom:12px;padding:16px;">
            <div class="rc-head">
              <span class="docid-badge">${m.doc_id}</span>
              <span class="cat-badge">${m.category || 'Garment'}</span>
              <button class="inspect-btn" data-doc-id="${m.doc_id}" style="margin-left:auto;">Inspect</button>
            </div>
            <h3 style="font-size:0.95rem;font-weight:700;margin:6px 0;">${m.title}</h3>
            <div style="margin-top:8px;">
              <span style="font-size:0.75rem;font-weight:700;color:var(--text-muted);display:block;margin-bottom:4px;">Positional Evidence:</span>
              <div class="token-grid">${pairsHtml}</div>
            </div>
          </div>
        `;
      }).join('');

      this.matchesBody.querySelectorAll('.inspect-btn').forEach(btn => {
        btn.addEventListener('click', () => onOpenDoc(btn.dataset.docId));
      });
    }
  }
}

window.TracerView = TracerView;
