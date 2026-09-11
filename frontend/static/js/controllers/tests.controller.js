/**
 * Tests Controller (Frontend)
 * ============================
 * Coordinates the Part E test suite execution and display.
 */

class TestsPageController {
  constructor(view, apiClient) {
    this.view = view || new window.TestsView();
    this.apiClient = apiClient || window.apiClient;
    this.init();
  }

  init() {
    if (this.view.refreshBtn) {
      this.view.refreshBtn.addEventListener('click', () => this.loadTests());
    }
    this.loadTests();
  }

  async loadTests() {
    this.view.showLoading();
    try {
      const data = await this.apiClient.getTestResults();
      this.view.renderTests(data);
    } catch (err) {
      if (this.view.tableWrap) {
        this.view.tableWrap.innerHTML = `<div class="error-msg">Failed to load tests: ${err.message}</div>`;
      }
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('tests-page')) {
    window.testsPageController = new TestsPageController();
  }
});
