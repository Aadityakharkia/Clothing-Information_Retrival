/**
 * Amazon-Style Search Autocomplete & Autofill Component
 * =====================================================
 * Provides real-time prefix completions, "in Category" scoped suggestions,
 * direct product previews, typo tolerance, recent search history,
 * and full keyboard navigation (arrows, Enter, Tab, Esc).
 */

(function () {
  const STORAGE_KEY = 'clothing_ir_recent_searches';
  const MAX_RECENTS = 6;

  class AmazonAutocomplete {
    constructor(inputElement, options = {}) {
      if (!inputElement) return;
      this.input = inputElement;
      this.form = inputElement.closest('form') || inputElement.closest('.search-pill-wrap') || inputElement.parentElement;
      this.options = Object.assign({
        limit: 8,
        minChars: 0,
        debounceMs: 120,
        onSelect: null
      }, options);

      this.dropdown = null;
      this.clearBtn = null;
      this.debounceTimer = null;
      this.cache = new Map();
      this.activeIdx = -1;
      this.currentItems = [];
      this.originalTypedValue = '';
      this.isOpen = false;

      this.init();
    }

    init() {
      // 1. Ensure wrapping element is position: relative
      const container = this.input.parentElement;
      if (container && window.getComputedStyle(container).position === 'static') {
        container.style.position = 'relative';
      }

      // 2. Add inline Clear button (x) inside input
      this.injectClearButton();

      // 3. Create dropdown element
      this.createDropdown();

      // 4. Attach event listeners
      this.attachEvents();
    }

    injectClearButton() {
      // Check if clear button already exists
      let btn = this.input.parentElement.querySelector('.search-clear-btn');
      if (!btn) {
        btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'search-clear-btn';
        btn.setAttribute('aria-label', 'Clear search text');
        btn.setAttribute('tabindex', '-1');
        btn.innerHTML = `
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        `;
        // Insert right after input
        this.input.insertAdjacentElement('afterend', btn);
      }
      this.clearBtn = btn;
      this.updateClearBtnVisibility();

      this.clearBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.input.value = '';
        this.updateClearBtnVisibility();
        this.input.focus();
        this.fetchSuggestions('');
      });
    }

    updateClearBtnVisibility() {
      if (this.clearBtn) {
        if (this.input.value.trim().length > 0) {
          this.clearBtn.classList.add('visible');
        } else {
          this.clearBtn.classList.remove('visible');
        }
      }
    }

    createDropdown() {
      let dd = this.form.querySelector('.amazon-autocomplete-dropdown');
      if (!dd) {
        dd = document.createElement('div');
        dd.className = 'amazon-autocomplete-dropdown';
        dd.setAttribute('role', 'listbox');
        dd.setAttribute('aria-label', 'Search suggestions');
        // Place right after the search pill or input container
        const targetContainer = this.input.closest('.search-pill') || this.input.closest('.sidebar-search') || this.input.parentElement;
        targetContainer.insertAdjacentElement('afterend', dd);
      }
      this.dropdown = dd;
    }

    attachEvents() {
      // Input event (debounced fetch)
      this.input.addEventListener('input', () => {
        this.updateClearBtnVisibility();
        this.originalTypedValue = this.input.value;
        this.activeIdx = -1;
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
          this.fetchSuggestions(this.input.value.trim());
        }, this.options.debounceMs);
      });

      // Focus event (show recents/popular or current suggestions)
      this.input.addEventListener('focus', () => {
        this.originalTypedValue = this.input.value;
        this.fetchSuggestions(this.input.value.trim());
      });

      // Keyboard navigation
      this.input.addEventListener('keydown', (e) => this.handleKeyDown(e));

      // Global click to close when clicking outside
      document.addEventListener('click', (e) => {
        if (!this.form.contains(e.target) && !this.dropdown.contains(e.target)) {
          this.closeDropdown();
        }
      });

      // Intercept form submit to save search to history
      if (this.form && this.form.tagName === 'FORM') {
        this.form.addEventListener('submit', () => {
          const q = this.input.value.trim();
          if (q) this.saveRecentSearch(q);
        });
      }
    }

    async fetchSuggestions(query) {
      const cacheKey = query.toLowerCase();

      // For empty query, synthesize recent + popular suggestions
      if (!query) {
        const recents = this.getRecentSearches();
        try {
          let popular = [];
          if (this.cache.has('__empty__')) {
            popular = this.cache.get('__empty__');
          } else if (window.apiClient && window.apiClient.getSuggestions) {
            const data = await window.apiClient.getSuggestions('', 8);
            popular = data.suggestions || [];
            this.cache.set('__empty__', popular);
          }
          this.renderEmptyState(recents, popular);
          this.openDropdown();
        } catch (err) {
          console.debug('[Autocomplete] Could not load empty suggestions:', err);
          if (recents.length > 0) {
            this.renderEmptyState(recents, []);
            this.openDropdown();
          } else {
            this.closeDropdown();
          }
        }
        return;
      }

      // Check client cache
      if (this.cache.has(cacheKey)) {
        this.renderData(this.cache.get(cacheKey), query);
        this.openDropdown();
        return;
      }

      try {
        if (!window.apiClient || !window.apiClient.getSuggestions) return;
        const data = await window.apiClient.getSuggestions(query, this.options.limit);
        this.cache.set(cacheKey, data);
        if (this.input.value.trim().toLowerCase() === cacheKey) {
          this.renderData(data, query);
          this.openDropdown();
        }
      } catch (err) {
        console.error('[Autocomplete Error]', err);
      }
    }

    renderEmptyState(recents, popular) {
      this.currentItems = [];
      this.activeIdx = -1;
      let html = '';

      // 1. Recent Searches Section
      if (recents.length > 0) {
        html += `
          <div class="auto-header">
            <span class="auto-header-title">
              <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              Recent Searches
            </span>
            <button type="button" class="auto-clear-history-btn" id="auto-clear-all-recents">Clear all</button>
          </div>
        `;

        recents.forEach((item, idx) => {
          const itemIdx = this.currentItems.length;
          this.currentItems.push({
            type: 'recent',
            text: item,
            query: item
          });
          html += `
            <div class="auto-item auto-item-recent" data-idx="${itemIdx}" role="option">
              <div class="auto-item-left">
                <svg class="auto-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>
                </svg>
                <span class="auto-text auto-recent-text">${this.escapeHtml(item)}</span>
              </div>
              <button type="button" class="auto-remove-recent-btn" data-recent="${this.escapeHtml(item)}" title="Remove from history" aria-label="Remove search">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
          `;
        });
      }

      // 2. Popular / Trending Recommendations
      if (popular.length > 0) {
        html += `
          <div class="auto-header ${recents.length > 0 ? 'mt-divider' : ''}">
            <span class="auto-header-title">
              <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
              Trending Garments
            </span>
          </div>
        `;

        popular.forEach(item => {
          const itemIdx = this.currentItems.length;
          this.currentItems.push({
            type: 'popular',
            text: item.text,
            query: item.text
          });
          html += `
            <div class="auto-item auto-item-popular" data-idx="${itemIdx}" role="option">
              <div class="auto-item-left">
                <svg class="auto-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <span class="auto-text">${this.escapeHtml(item.text)}</span>
              </div>
              <span class="auto-badge">Popular</span>
            </div>
          `;
        });
      }

      this.dropdown.innerHTML = html;
      this.bindDropdownClicks();
    }

    renderData(data, query) {
      this.currentItems = [];
      this.activeIdx = -1;
      const suggestions = data.suggestions || [];
      const products = data.products || [];
      const correctedFrom = data.corrected_from;

      if (suggestions.length === 0 && products.length === 0) {
        this.closeDropdown();
        return;
      }

      let html = '';

      // Typo correction note if applicable
      if (correctedFrom) {
        html += `
          <div class="auto-typo-notice">
            <span>Did you mean: <strong style="color:var(--accent);">${this.escapeHtml(data.query)}</strong>?</span>
          </div>
        `;
      }

      // Query & Category Suggestions
      suggestions.forEach(item => {
        const itemIdx = this.currentItems.length;
        const isScope = item.type === 'category_scope';

        this.currentItems.push({
          type: item.type,
          text: item.text,
          query: item.text,
          category: item.category || null
        });

        // Amazon highlight formatting:
        // display_prefix (regular) + display_completion (bold)
        let formattedText = '';
        if (item.display_prefix && item.display_completion) {
          formattedText = `<span class="auto-prefix">${this.escapeHtml(item.display_prefix)}</span><strong class="auto-bold">${this.escapeHtml(item.display_completion)}</strong>`;
        } else {
          formattedText = `<span class="auto-prefix">${this.escapeHtml(item.displayText || item.text)}</span>`;
        }

        if (isScope) {
          html += `
            <div class="auto-item auto-item-scope" data-idx="${itemIdx}" role="option">
              <div class="auto-item-left">
                <svg class="auto-icon auto-icon-dept" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/>
                </svg>
                <div class="auto-scope-wrap">
                  <span class="auto-text">${formattedText}</span>
                  <span class="auto-scope-tag">${this.escapeHtml(item.category)}</span>
                </div>
              </div>
              <svg class="auto-arrow-right" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </div>
          `;
        } else {
          html += `
            <div class="auto-item" data-idx="${itemIdx}" role="option">
              <div class="auto-item-left">
                <svg class="auto-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <span class="auto-text">${formattedText}</span>
              </div>
            </div>
          `;
        }
      });

      // Matching Products section (Amazon Rich Autocomplete)
      if (products.length > 0) {
        html += `
          <div class="auto-header mt-divider">
            <span class="auto-header-title">
              <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                <line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path>
              </svg>
              Matching Garments
            </span>
          </div>
          <div class="auto-products-container">
        `;

        products.forEach(prod => {
          const itemIdx = this.currentItems.length;
          this.currentItems.push({
            type: 'product',
            text: prod.title,
            query: prod.title,
            docId: prod.doc_id,
            category: prod.category
          });

          html += `
            <div class="auto-product-row" data-idx="${itemIdx}" data-doc-id="${prod.doc_id}" role="option">
              <img class="auto-prod-thumb" src="${prod.image_url}" alt="${this.escapeHtml(prod.title)}" onerror="this.src='https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?auto=format&fit=crop&w=150&q=80'">
              <div class="auto-prod-info">
                <div class="auto-prod-title">${this.escapeHtml(prod.title)}</div>
                <div class="auto-prod-meta">
                  <span class="auto-prod-cat">${this.escapeHtml(prod.category)}</span>
                  <span class="auto-prod-id">${this.escapeHtml(prod.doc_id)}</span>
                </div>
              </div>
              <button type="button" class="auto-prod-inspect-btn" data-doc-id="${prod.doc_id}" title="Quick inspect garment">
                Inspect
              </button>
            </div>
          `;
        });

        html += `</div>`;
      }

      this.dropdown.innerHTML = html;
      this.bindDropdownClicks();
    }

    bindDropdownClicks() {
      // 1. Suggestion items click
      this.dropdown.querySelectorAll('.auto-item').forEach(el => {
        el.addEventListener('click', (e) => {
          // If clicked remove recent button, do not select item
          if (e.target.closest('.auto-remove-recent-btn')) return;

          const idx = parseInt(el.getAttribute('data-idx'), 10);
          this.selectItem(idx);
        });

        // Mouse hover synchronizes active index
        el.addEventListener('mouseenter', () => {
          const idx = parseInt(el.getAttribute('data-idx'), 10);
          this.setActiveItem(idx, false);
        });
      });

      // 2. Product rows click
      this.dropdown.querySelectorAll('.auto-product-row').forEach(el => {
        el.addEventListener('click', (e) => {
          // If inspect button was clicked specifically, open document modal
          const inspectBtn = e.target.closest('.auto-prod-inspect-btn');
          if (inspectBtn) {
            e.stopPropagation();
            const docId = inspectBtn.getAttribute('data-doc-id');
            this.closeDropdown();
            if (window.openDocModal) window.openDocModal(docId);
            return;
          }

          const idx = parseInt(el.getAttribute('data-idx'), 10);
          this.selectItem(idx);
        });

        el.addEventListener('mouseenter', () => {
          const idx = parseInt(el.getAttribute('data-idx'), 10);
          this.setActiveItem(idx, false);
        });
      });

      // 3. Remove single recent item button
      this.dropdown.querySelectorAll('.auto-remove-recent-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const targetItem = btn.getAttribute('data-recent');
          this.removeRecentSearch(targetItem);
          // Re-render empty state with updated recents
          this.fetchSuggestions('');
        });
      });

      // 4. Clear all recents button
      const clearAllBtn = this.dropdown.querySelector('#auto-clear-all-recents');
      if (clearAllBtn) {
        clearAllBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          this.clearRecentSearches();
          this.fetchSuggestions('');
        });
      }
    }

    handleKeyDown(e) {
      if (!this.isOpen && (e.key === 'ArrowDown' || e.key === 'ArrowUp')) {
        this.fetchSuggestions(this.input.value.trim());
        return;
      }

      if (!this.isOpen) return;

      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          this.moveActive(1);
          break;

        case 'ArrowUp':
          e.preventDefault();
          this.moveActive(-1);
          break;

        case 'Enter':
          if (this.activeIdx >= 0 && this.activeIdx < this.currentItems.length) {
            e.preventDefault();
            this.selectItem(this.activeIdx);
          } else {
            const q = this.input.value.trim();
            if (q) this.saveRecentSearch(q);
            this.closeDropdown();
          }
          break;

        case 'Tab':
          // Auto-fill input text with current selection or first suggestion
          if (this.currentItems.length > 0) {
            const targetIdx = this.activeIdx >= 0 ? this.activeIdx : 0;
            const item = this.currentItems[targetIdx];
            if (item && item.query) {
              e.preventDefault();
              this.input.value = item.query;
              this.originalTypedValue = item.query;
              this.updateClearBtnVisibility();
              this.fetchSuggestions(item.query);
            }
          }
          break;

        case 'Escape':
          e.preventDefault();
          this.closeDropdown();
          this.input.value = this.originalTypedValue;
          this.updateClearBtnVisibility();
          break;
      }
    }

    moveActive(delta) {
      const total = this.currentItems.length;
      if (total === 0) return;

      let newIdx = this.activeIdx + delta;

      if (newIdx >= total) {
        newIdx = -1; // wrap back to user's typed input
      } else if (newIdx < -1) {
        newIdx = total - 1;
      }

      this.setActiveItem(newIdx, true);
    }

    setActiveItem(idx, updateInput = false) {
      this.activeIdx = idx;

      // Update active classes
      const elements = this.dropdown.querySelectorAll('[data-idx]');
      elements.forEach(el => {
        const elIdx = parseInt(el.getAttribute('data-idx'), 10);
        if (elIdx === idx) {
          el.classList.add('active');
          el.setAttribute('aria-selected', 'true');
          el.scrollIntoView({ block: 'nearest' });
        } else {
          el.classList.remove('active');
          el.removeAttribute('aria-selected');
        }
      });

      // Update input preview if triggered by keyboard
      if (updateInput) {
        if (idx >= 0 && idx < this.currentItems.length) {
          this.input.value = this.currentItems[idx].query;
        } else {
          this.input.value = this.originalTypedValue;
        }
        this.updateClearBtnVisibility();
      }
    }

    selectItem(idx) {
      if (idx < 0 || idx >= this.currentItems.length) return;
      const item = this.currentItems[idx];
      const selectedQuery = item.query;

      this.input.value = selectedQuery;
      this.updateClearBtnVisibility();
      this.saveRecentSearch(selectedQuery);
      this.closeDropdown();

      // If custom onSelect handler exists
      if (typeof this.options.onSelect === 'function') {
        this.options.onSelect(item);
        return;
      }

      // Check current page context:
      // If we are on Results page (/results), use router or controller to re-search
      if (window.location.pathname.includes('/results') && window.resultsPageController) {
        const sidebarInput = document.getElementById('sidebar-query-input');
        if (sidebarInput) sidebarInput.value = selectedQuery;
        const sidebarBtn = document.getElementById('sidebar-search-btn');
        if (sidebarBtn) {
          sidebarBtn.click();
          return;
        }
      }

      // Otherwise submit the parent form or navigate
      if (this.form && this.form.tagName === 'FORM') {
        this.form.submit();
      } else {
        const modeHidden = document.getElementById('mode-hidden');
        const mode = modeHidden ? modeHidden.value : 'vsm';
        window.location.href = `/results?q=${encodeURIComponent(selectedQuery)}&mode=${mode}`;
      }
    }

    openDropdown() {
      if (!this.isOpen) {
        this.dropdown.classList.add('show');
        this.isOpen = true;
      }
    }

    closeDropdown() {
      if (this.isOpen) {
        this.dropdown.classList.remove('show');
        this.isOpen = false;
        this.activeIdx = -1;
      }
    }

    // ── Local Storage History ──────────────────────────────────────────

    getRecentSearches() {
      try {
        const stored = localStorage.getItem(STORAGE_KEY);
        return stored ? JSON.parse(stored) : [];
      } catch (e) {
        return [];
      }
    }

    saveRecentSearch(query) {
      if (!query || typeof query !== 'string') return;
      const clean = query.trim();
      if (!clean) return;

      try {
        let recents = this.getRecentSearches();
        recents = recents.filter(item => item.toLowerCase() !== clean.toLowerCase());
        recents.unshift(clean);
        if (recents.length > MAX_RECENTS) {
          recents = recents.slice(0, MAX_RECENTS);
        }
        localStorage.setItem(STORAGE_KEY, JSON.stringify(recents));
      } catch (e) {
        console.debug('Failed to write recent search:', e);
      }
    }

    removeRecentSearch(targetItem) {
      try {
        let recents = this.getRecentSearches();
        recents = recents.filter(item => item !== targetItem);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(recents));
      } catch (e) {
        console.debug('Failed to remove recent search:', e);
      }
    }

    clearRecentSearches() {
      try {
        localStorage.removeItem(STORAGE_KEY);
      } catch (e) {
        console.debug('Failed to clear recent searches:', e);
      }
    }

    escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }
  }

  // Auto-initialize on search inputs across the application
  function setupAutocompletes() {
    // 1. Home Search Bar
    const mainSearchInput = document.getElementById('main-search-input');
    if (mainSearchInput && !mainSearchInput._amazonAutocomplete) {
      mainSearchInput._amazonAutocomplete = new AmazonAutocomplete(mainSearchInput);
    }

    // 2. Sidebar Refine Search Bar (Results Page)
    const sidebarInput = document.getElementById('sidebar-query-input');
    if (sidebarInput && !sidebarInput._amazonAutocomplete) {
      sidebarInput._amazonAutocomplete = new AmazonAutocomplete(sidebarInput, {
        onSelect: (item) => {
          sidebarInput.value = item.query;
          const sidebarBtn = document.getElementById('sidebar-search-btn');
          if (sidebarBtn) sidebarBtn.click();
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupAutocompletes);
  } else {
    setupAutocompletes();
  }

  window.AmazonAutocomplete = AmazonAutocomplete;
})();
