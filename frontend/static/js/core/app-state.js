/**
 * Application State Store
 * =======================
 * Minimalist reactive store for tracking client-side state,
 * active filters, current request tokens, and latency telemetry.
 */

class AppState {
  constructor() {
    this.state = {
      activeRoute: window.location.pathname,
      lastRequestToken: null,
      lastResponseTimeMs: null,
      recentTokens: [],
      currentSearch: {
        query: '',
        mode: 'vsm',
        topK: 10,
        lambda: 0.5
      },
      activeDocModalId: null
    };
    this.listeners = new Set();
  }

  get(key) {
    return this.state[key];
  }

  set(key, value) {
    this.state[key] = value;
    this.notify(key, value);
  }

  update(patch) {
    Object.assign(this.state, patch);
    for (const [key, value] of Object.entries(patch)) {
      this.notify(key, value);
    }
  }

  recordRequestToken(token, latencyMs) {
    if (!token) return;
    this.state.lastRequestToken = token;
    this.state.lastResponseTimeMs = latencyMs;
    this.state.recentTokens.unshift({
      token,
      latencyMs,
      timestamp: new Date().toISOString()
    });
    if (this.state.recentTokens.length > 20) {
      this.state.recentTokens.pop();
    }
    this.notify('lastRequestToken', token);
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notify(key, value) {
    for (const listener of this.listeners) {
      try {
        listener(key, value, this.state);
      } catch (err) {
        console.error('[AppState] Error in listener:', err);
      }
    }
  }
}

// Global singleton instance
window.appState = new AppState();
