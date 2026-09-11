/**
 * Results Controller (Frontend)
 * ==============================
 * Orchestrates search execution, proximity boost toggle, and Rocchio feedback.
 */

class ResultsPageController {
  constructor(view, apiClient, router) {
    this.view = view || new window.ResultsView();
    this.apiClient = apiClient || window.apiClient;
    this.router = router || window.appRouter;

    this.query = this.router.getParam('q', '');
    this.mode = this.router.getParam('mode', 'vsm');
    this.relevantDocIds = new Set();
    this.originalResults = [];
    this.isBoostActive = false;

    this.init();
  }

  async init() {
    this.attachSidebarEvents();
    if (this.query) {
      await this.executeSearch();
    } else {
      this.view.showEmpty('');
    }
  }

  attachSidebarEvents() {
    // Mode chips
    document.querySelectorAll('.mode-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const selectedMode = chip.dataset.mode;
        if (selectedMode !== this.mode) {
          this.mode = selectedMode;
          this.router.setParam('mode', selectedMode);
          this.router.updateUrlWithoutReload();
          document.querySelectorAll('.mode-chip').forEach(c => c.classList.remove('active'));
          chip.classList.add('active');
          if (this.view.modeBadge) this.view.modeBadge.textContent = selectedMode.toUpperCase();

          const vsmInnovations = document.getElementById('vsm-innovations');
          if (vsmInnovations) {
            vsmInnovations.style.display = (selectedMode === 'vsm' || selectedMode === 'hybrid') ? 'block' : 'none';
          }
          this.executeSearch();
        }
      });
    });

    // Refine search input
    const sidebarInput = document.getElementById('sidebar-query-input');
    const sidebarBtn = document.getElementById('sidebar-search-btn');
    if (sidebarBtn && sidebarInput) {
      const triggerNewSearch = () => {
        const newQuery = sidebarInput.value.trim();
        if (newQuery) {
          this.query = newQuery;
          this.router.setParam('q', newQuery);
          this.router.updateUrlWithoutReload();
          if (this.view.qDisplay) this.view.qDisplay.textContent = `"${newQuery}"`;
          this.relevantDocIds.clear();
          this.view.updateSelectionCount(0);
          this.executeSearch();
        }
      };
      sidebarBtn.addEventListener('click', triggerNewSearch);
      sidebarInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') triggerNewSearch();
      });
    }

    // Proximity Boost toggle (IR Idea 1)
    const boostToggle = document.getElementById('toggle-proximity-boost');
    if (boostToggle) {
      boostToggle.addEventListener('change', () => {
        this.isBoostActive = boostToggle.checked;
        this.executeSearch();
      });
    }

    // 1-Click PRF (IR Idea 3)
    const prfBtn = document.getElementById('prf-btn');
    if (prfBtn) {
      prfBtn.addEventListener('click', async () => {
        await this.executeRocchio(true);
      });
    }

    // Apply Rocchio (user selected)
    const rocchioBtn = document.getElementById('rocchio-btn');
    if (rocchioBtn) {
      rocchioBtn.addEventListener('click', async () => {
        await this.executeRocchio(false);
      });
    }

    // Reset Feedback
    const resetBtn = document.getElementById('reset-btn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        this.relevantDocIds.clear();
        this.view.updateSelectionCount(0);
        this.view.renderExpandedTerms([]);
        this.view.renderResults(
          this.originalResults,
          this.mode,
          this.query,
          (id, checked) => this.handleDocSelection(id, checked),
          (id) => window.openDocModal(id)
        );
        resetBtn.style.display = 'none';
      });
    }
  }

  async executeSearch() {
    this.view.showLoading();
    try {
      let response;
      if (this.mode === 'phrase') {
        response = await this.apiClient.searchPositional(this.query);
      } else if (this.mode === 'proximity') {
        response = await this.apiClient.searchPositional(this.query);
      } else {
        // VSM or Hybrid
        if (this.isBoostActive) {
          response = await this.apiClient.searchHybrid(this.query, 0.5, 10);
        } else {
          response = await this.apiClient.searchVSM(this.query, 10);
        }
      }

      this.originalResults = response.results || [];
      this.view.renderResults(
        this.originalResults,
        this.isBoostActive ? 'hybrid' : this.mode,
        this.query,
        (id, checked) => this.handleDocSelection(id, checked),
        (id) => window.openDocModal(id)
      );
    } catch (err) {
      if (this.view.listContainer) {
        this.view.listContainer.innerHTML = `<div class="error-msg">Error executing search: ${err.message}</div>`;
      }
    }
  }

  handleDocSelection(docId, isChecked) {
    if (isChecked) {
      this.relevantDocIds.add(docId);
    } else {
      this.relevantDocIds.delete(docId);
    }
    this.view.updateSelectionCount(this.relevantDocIds.size);
  }

  async executeRocchio(isPrf) {
    this.view.showLoading();
    try {
      const payload = {
        query: this.query,
        relevant_doc_ids: Array.from(this.relevantDocIds),
        irrelevant_doc_ids: [],
        is_prf: isPrf,
        top_k: 10
      };
      const response = await this.apiClient.submitRocchioFeedback(payload);
      this.view.renderExpandedTerms(response.top_expanded_terms || []);
      this.view.renderResults(
        response.results || [],
        'vsm',
        this.query,
        (id, checked) => this.handleDocSelection(id, checked),
        (id) => window.openDocModal(id)
      );
    } catch (err) {
      alert(`Feedback execution failed: ${err.message}`);
      this.view.renderResults(this.originalResults, this.mode, this.query, null, (id) => window.openDocModal(id));
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('results-page')) {
    window.resultsPageController = new ResultsPageController();
  }
});
