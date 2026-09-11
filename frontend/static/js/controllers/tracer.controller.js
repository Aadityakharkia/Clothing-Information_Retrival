/**
 * Tracer Controller (Frontend)
 * =============================
 * Orchestrates step-by-step positional intersection simulation.
 */

class TracerPageController {
  constructor(view, apiClient) {
    this.view = view || new window.TracerView();
    this.apiClient = apiClient || window.apiClient;
    this.init();
  }

  init() {
    if (this.view.traceBtn) {
      this.view.traceBtn.addEventListener('click', () => this.runTrace());
    }

    // Attach presets
    document.querySelectorAll('.preset-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const t1 = chip.dataset.t1;
        const t2 = chip.dataset.t2;
        const k = chip.dataset.k;
        this.view.setInputs(t1, t2, k);
        this.runTrace();
      });
    });

    // Run initial trace on page load
    this.runTrace();
  }

  async runTrace() {
    const { term1, term2, k } = this.view.getInputs();
    if (!term1 || !term2) {
      alert('Please enter two terms to trace positional intersection.');
      return;
    }

    this.view.showLoading();
    try {
      const data = await this.apiClient.traceIntersection(term1, term2, k);
      this.view.renderTraceResults(data, (docId) => window.openDocModal(docId));
    } catch (err) {
      if (this.view.terminalBody) {
        this.view.terminalBody.innerHTML = `<span class="log-warn">Trace error: ${err.message}</span>`;
      }
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('tracer-page')) {
    window.tracerPageController = new TracerPageController();
  }
});
