/**
 * Search Controller (Frontend)
 * =============================
 * Coordinates user input on the Search Home page, chips, and triggers navigation.
 */

class SearchPageController {
  constructor(view, router) {
    this.view = view || new window.SearchView();
    this.router = router || window.appRouter;
    this.init();
  }

  init() {
    if (this.view.searchForm) {
      this.view.searchForm.addEventListener('submit', (e) => {
        const query = this.view.getQuery();
        if (!query) {
          e.preventDefault();
        }
      });
    }

    // Attach click events for sample chips
    document.querySelectorAll('.sample-q, .preset-chip, .suggestion-chip').forEach(chip => {
      chip.addEventListener('click', (e) => {
        e.preventDefault();
        const query = chip.dataset.q || chip.textContent.trim().replace(/^["']|["']$/g, '');
        const mode = chip.dataset.mode || 'vsm';
        this.view.setQuery(query);
        const modeHidden = document.getElementById('mode-hidden');
        if (modeHidden) modeHidden.value = mode;
        this.router.navigateToResults(query, mode);
      });
    });

    this.view.focusInput();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('search-page') || document.getElementById('main-search-input')) {
    window.searchPageController = new SearchPageController();
  }
});
