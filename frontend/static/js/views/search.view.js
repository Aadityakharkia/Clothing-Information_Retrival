/**
 * Search View (Pure DOM Rendering)
 * ================================
 */

class SearchView {
  constructor() {
    this.searchInput = document.getElementById('main-search-input') || document.getElementById('search-input');
    this.searchForm = document.getElementById('search-form');
    this.chipContainer = document.querySelector('.sample-qs') || document.querySelector('.search-chips');
  }

  getQuery() {
    return this.searchInput ? this.searchInput.value.trim() : '';
  }

  setQuery(query) {
    if (this.searchInput) {
      this.searchInput.value = query;
    }
  }

  focusInput() {
    if (this.searchInput) {
      this.searchInput.focus();
    }
  }
}

window.SearchView = SearchView;
