/**
 * Vocabulary Controller (Frontend)
 * ================================
 * Coordinates the Index Explorer dictionary view and filtering.
 */

class VocabPageController {
  constructor(view, apiClient) {
    this.view = view || new window.VocabView();
    this.apiClient = apiClient || window.apiClient;
    this.allTerms = [];
    this.init();
  }

  init() {
    if (this.view.refreshBtn) {
      this.view.refreshBtn.addEventListener('click', () => this.loadVocab());
    }

    if (this.view.filterInput) {
      this.view.filterInput.addEventListener('input', () => {
        const query = this.view.getFilterValue();
        if (!query) {
          this.view.renderTable(this.allTerms);
        } else {
          const filtered = this.allTerms.filter(t => t.term.toLowerCase().includes(query));
          this.view.renderTable(filtered);
        }
      });
    }

    this.loadVocab();
  }

  async loadVocab() {
    this.view.showLoading();
    try {
      const data = await this.apiClient.getVocabulary('', 1, 2000);
      this.allTerms = data.terms || data.items || [];
      this.view.renderTable(this.allTerms);
    } catch (err) {
      if (this.view.tableWrap) {
        this.view.tableWrap.innerHTML = `<div class="error-msg">Failed to load vocabulary index: ${err.message}</div>`;
      }
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('vocab-page')) {
    window.vocabPageController = new VocabPageController();
  }
});
