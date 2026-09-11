# Architecture & System Steering Document
## Clothing Information Retrieval Engine (CSD358)
**Lead Architect & Senior Engineering Steering Guidelines**

---

## 1. System Vision & Architecture Principles

The **Clothing Information Retrieval Engine** is an enterprise-grade Information Retrieval research and production platform built strictly on classic and advanced IR algorithms (lnc.ltc Vector Space Model, Positional Inverted Indexing, Phrase / Proximity verification, Hybrid Proximity Boosting, Rocchio Relevance Feedback, and Positional Intersection Tracing).

### Core Architectural Tenets:
1. **Clean Layered Separation (Clean Architecture / MVC)**:
   - **Frontend (Presentation Tier)**: Pure decoupled client layer. Router handles URL history and view switching. Controllers orchestrate asynchronous API fetching and state management. Views execute atomic, deterministic DOM rendering.
   - **Backend (API & Application Tier)**: Flask application factory with Blueprint routing. HTTP concerns terminate at Controllers. Business IR operations are purely encapsulated in stateless/singleton Services. Typed data contracts are guaranteed by Models.
   - **Data Tier**: Inverted index, positional index, and corpus files strictly separated from runtime logic.
2. **Request Tokenization & Full Observability**:
   - Every incoming HTTP request (page or API) is stamped with a unique monotonic/UUID tracing token: `REQ-XXXXXX`.
   - The token is propagated across headers (`X-Request-Token`), injected into Flask `g`, and logged into `output/request_log.jsonl` with latency, IP, method, and query parameters.
   - The frontend API client extracts and tracks this token for end-to-end auditability and debugging.
3. **Algorithmic Purity & Immutability**:
   - Standard IR formulations (Porter Stemmer, TF-IDF lnc.ltc, positional lists) remain intact with zero synthetic/AI dependencies.

---

## 2. Directory Hierarchy

```
Clothing-Information_Retrival/
│
├── ARCHITECTURE.md                  ← Steering file (Always consult before modifications)
├── pytest.ini                       ← Pytest configuration
├── README.md                        ← Project overview & runbook
│
├── backend/                         ← All Server-side Python logic
│   ├── server.py                    ← Application runner & CLI entry point
│   ├── config.py                    ← Environment configuration (Dev/Prod/Test)
│   │
│   ├── app/                         ← Core Flask Application Factory
│   │   ├── __init__.py              ← create_app() factory
│   │   │
│   │   ├── middleware/              ← Request lifecycle & Cross-cutting concerns
│   │   │   ├── __init__.py
│   │   │   ├── request_tracker.py   ← Request tokenization & JSONL telemetry logger
│   │   │   └── error_handler.py     ← RFC 7807 compliant error handler
│   │   │
│   │   ├── models/                  ← Typed data structures & contracts
│   │   │   ├── __init__.py
│   │   │   ├── document.py          ← Document entity model
│   │   │   ├── query.py             ← Query request/response payloads
│   │   │   └── request_token.py     ← Trace context model
│   │   │
│   │   ├── routes/                  ← Flask Blueprints (Routing only)
│   │   │   ├── __init__.py
│   │   │   ├── page_routes.py       ← Jinja2 Page templates routing (/, /results, /tracer...)
│   │   │   └── api_routes.py        ← REST API endpoints (/api/*)
│   │   │
│   │   ├── controllers/             ← Controller layer (Input parsing, orchestration)
│   │   │   ├── __init__.py
│   │   │   ├── search_controller.py ← VSM & Positional phrase search orchestration
│   │   │   ├── tracer_controller.py ← Inverted index step-by-step trace runner
│   │   │   ├── feedback_controller.py← Rocchio PRF algorithm orchestration
│   │   │   ├── tests_controller.py  ← Assignment Part E test runner API
│   │   │   └── vocab_controller.py  ← Vocabulary dictionary & postings inspection
│   │   │
│   │   └── services/                ← Domain IR Engine (Pure Python, Framework Agnostic)
│   │       ├── __init__.py
│   │       ├── preprocessor.py      ← Tokenization, case folding, stopwords, Porter Stemmer
│   │       ├── indexer.py           ← ClothingCorpusIndex (Inverted & Positional builder)
│   │       ├── vsm_service.py       ← lnc.ltc Vector Space Model scoring
│   │       ├── positional_service.py← Exact phrase & ordered proximity (WITHIN/k) search
│   │       └── advanced_ir.py       ← Hybrid proximity boost, Positional Tracer, Rocchio PRF
│   │
│   └── scripts/                     ← Standalone DevOps / IR CLI scripts
│       ├── build_index.py           ← Corpus index compilation script
│       ├── run_tests.py             ← CLI test suite runner
│       └── export.py                ← Packaging & deliverables bundle generator
│
├── frontend/                        ← Client-side Presentation Tier
│   ├── templates/                   ← Jinja2 Multi-page templates
│   │   ├── base.html                ← Master layout with header/nav/footer
│   │   ├── search.html              ← Home search page (Syne aesthetic)
│   │   ├── results.html             ← Search results & ranking comparison
│   │   ├── tracer.html              ← Positional intersection step tracer
│   │   ├── tests.html               ← Part E automated test results view
│   │   └── index_explorer.html      ← Vocabulary & postings table
│   │
│   └── static/
│       ├── css/
│       │   └── style.css            ← Curated premium styling & typography
│       └── js/
│           ├── core/                ← Framework core
│           │   ├── router.js        ← Client router & navigation manager
│           │   ├── api-client.js    ← Centralized Fetch client with token injection
│           │   └── app-state.js     ← Reactive state store
│           │
│           ├── controllers/         ← Frontend Page Controllers
│           │   ├── search.controller.js
│           │   ├── results.controller.js
│           │   ├── tracer.controller.js
│           │   ├── tests.controller.js
│           │   └── vocab.controller.js
│           │
│           └── views/               ← Frontend DOM Views (Pure Rendering)
│               ├── search.view.js
│               ├── results.view.js
│               ├── tracer.view.js
│               ├── tests.view.js
│               └── vocab.view.js
│
├── data/
│   └── corpus.txt                   ← Raw documents corpus (D001-D100)
├── output/                          ← Index artifacts & request audit log
│   ├── inverted_index.json
│   ├── positional_index.json
│   └── request_log.jsonl            ← Request tokenization trace stream
├── tests/                           ← Automated pytest suite
│   └── test_ir_engine.py
└── src/                             ← Backward-compatibility facade for tests
```

---

## 3. Request Tokenization & Telemetry Specification

Every request through the system passes through the `RequestTrackerMiddleware`:

1. **Token Generation**: Format `REQ-<HEX6>` (e.g. `REQ-8B4E1F`).
2. **Context Binding**: Stored in Flask `flask.g.request_token` and `flask.g.start_time`.
3. **Response Headers**:
   - `X-Request-Token`: The unique token identifier.
   - `X-Response-Time-Ms`: Execution duration in milliseconds.
4. **Structured Audit Log**:
   Appended atomically to `output/request_log.jsonl`:
   ```json
   {
     "token": "REQ-8B4E1F",
     "timestamp": "2026-09-11T12:30:00.123Z",
     "method": "GET",
     "path": "/api/search/vsm",
     "query": "cotton crew neck",
     "status": 200,
     "duration_ms": 8.4,
     "client_ip": "127.0.0.1"
   }
   ```
5. **Client Correlation**:
   The frontend `ApiClient` stores the token and displays it in debug toolbars, console logs, and tracer panels so developers can immediately link a UI query to its exact backend server execution record.

---

## 4. Coding Standards & Maintenance Protocol
1. **Never bypass Controllers**: Blueprints MUST only parse query parameters/bodies and invoke the respective controller.
2. **Never mix DOM manipulation into Controllers**: Frontend controllers only handle state and events; DOM manipulation must strictly live in `views/*.view.js`.
3. **Deterministic IR Outputs**: Inverted and positional indices must produce deterministic ordering with doc_id tie-breaking.
