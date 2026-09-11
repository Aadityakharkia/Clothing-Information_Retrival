/**
 * Client-Side Router & Navigation Manager
 * =======================================
 * Manages URL queries, browser history pushes, and active page coordination.
 */

class AppRouter {
  constructor() {
    this.currentPath = window.location.pathname;
    this.queryParams = new URLSearchParams(window.location.search);
  }

  getParam(key, defaultValue = '') {
    return this.queryParams.get(key) || defaultValue;
  }

  setParam(key, value) {
    if (value === undefined || value === null || value === '') {
      this.queryParams.delete(key);
    } else {
      this.queryParams.set(key, value);
    }
  }

  navigate(url) {
    window.location.href = url;
  }

  navigateToResults(query, mode = 'vsm') {
    const params = new URLSearchParams();
    if (query) params.set('q', query);
    if (mode && mode !== 'vsm') params.set('mode', mode);
    this.navigate(`/results?${params.toString()}`);
  }

  updateUrlWithoutReload() {
    const newUrl = `${window.location.pathname}?${this.queryParams.toString()}`;
    window.history.replaceState({}, '', newUrl);
  }
}

// Global singleton instance
window.appRouter = new AppRouter();
