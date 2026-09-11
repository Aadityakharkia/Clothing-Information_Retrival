/**
 * Centralized API Client with Request Tokenization
 * =================================================
 * Intercepts all outgoing HTTP requests, manages headers,
 * extracts X-Request-Token audit headers, and tracks latency telemetry.
 */

class ApiClient {
  constructor(baseUrl = '/api') {
    this.baseUrl = baseUrl;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Accept': 'application/json',
      ...(options.headers || {})
    };

    if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
      options.body = JSON.stringify(options.body);
    }

    const startTime = performance.now();
    try {
      const response = await fetch(url, { ...options, headers });
      const durationMs = Math.round(performance.now() - startTime);

      // Extract telemetry headers
      const requestToken = response.headers.get('X-Request-Token');
      const serverLatency = response.headers.get('X-Response-Time-Ms');

      if (requestToken && window.appState) {
        window.appState.recordRequestToken(requestToken, serverLatency || durationMs);
        console.debug(`[ApiClient] ${options.method || 'GET'} ${endpoint} -> ${response.status} [Token: ${requestToken}] (${durationMs}ms)`);
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `Request failed with HTTP status ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (err) {
      console.error(`[ApiClient Error] ${endpoint}:`, err);
      throw err;
    }
  }

  // Domain-specific IR methods
  searchVSM(query, topK = 10) {
    const params = new URLSearchParams({ q: query, top_k: topK });
    return this.request(`/search/vsm?${params.toString()}`);
  }

  searchPositional(query) {
    const params = new URLSearchParams({ q: query });
    return this.request(`/search/positional?${params.toString()}`);
  }

  searchHybrid(query, lambdaParam = 0.5, topK = 10) {
    const params = new URLSearchParams({ q: query, lambda: lambdaParam, top_k: topK });
    return this.request(`/search/hybrid?${params.toString()}`);
  }

  traceIntersection(term1, term2, k = 4) {
    const params = new URLSearchParams({ term1, term2, k });
    return this.request(`/trace?${params.toString()}`);
  }

  submitRocchioFeedback(payload) {
    return this.request('/feedback', {
      method: 'POST',
      body: payload
    });
  }

  getTestResults() {
    return this.request('/tests');
  }

  getVocabulary(search = '', page = 1, perPage = 50) {
    const params = new URLSearchParams({ search, page, per_page: perPage });
    return this.request(`/vocabulary?${params.toString()}`);
  }

  getDocumentDetails(docId) {
    return this.request(`/doc/${encodeURIComponent(docId)}`);
  }
}

// Global singleton instance
window.apiClient = new ApiClient();
