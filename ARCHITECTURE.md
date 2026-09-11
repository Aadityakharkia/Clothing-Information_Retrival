# Architecture & System Steering Document
## Clothing Information Retrieval Engine (CSD358)

---

## 1. System Overview

The **Clothing Information Retrieval Engine** is a full-stack Flask web application implementing classic and advanced IR algorithms against a 100-document clothing product corpus.

**IR Algorithms:** lnc.ltc Vector Space Model · Positional Inverted Indexing · Phrase Search · Proximity Verification · Hybrid Proximity Boosting · Rocchio Relevance Feedback · Semantic Search (sentence-transformers)

---

## 2. Architectural Principles

### Clean Layered Separation (MVC / Clean Architecture)

| Layer | Responsibility |
|---|---|
| **Frontend — Views** | Pure DOM rendering (`views/*.view.js`). Zero business logic. |
| **Frontend — Controllers** | Event handling, API calls, state management (`controllers/*.controller.js`). Zero DOM code. |
| **Backend — Routes** | HTTP parameter parsing only. Immediately delegates to Controllers. No logic. |
| **Backend — Controllers** | Orchestrates service calls, composes response payloads. |
| **Backend — Services** | Pure Python IR algorithms. Framework-agnostic. Singleton-cached. |
| **Backend — Models** | Typed data contracts: `Document`, `Query`, `RequestTrace`. |
| **Data** | Corpus file and runtime index artifacts. Strictly separated from application logic. |

### Request Tokenization & Observability
Every HTTP request is stamped with a unique token (`REQ-<HEX6>`), stored in Flask `g`, returned in response headers (`X-Request-Token`, `X-Response-Time-Ms`), and appended to `output/request_log.jsonl`.

---

## 3. Directory Structure

```
Clothing-Information_Retrival/
│
├── package.json                    ← npm run dev / start / setup
├── requirements.txt                ← Python dependencies
├── README.md                       ← Runbook & API reference
├── ARCHITECTURE.md                 ← This file
│
├── backend/                        ← All server-side Python
│   ├── server.py                   ← Application entry point
│   ├── config.py                   ← Dev / Prod / Test configuration
│   │
│   └── app/                        ← Flask Application Factory
│       ├── __init__.py             ← create_app()
│       │
│       ├── middleware/             ← Cross-cutting concerns
│       │   ├── __init__.py
│       │   ├── request_tracker.py  ← Token generation & JSONL audit log
│       │   └── error_handler.py    ← RFC 7807 structured error responses
│       │
│       ├── models/                 ← Typed data contracts
│       │   ├── __init__.py
│       │   ├── document.py         ← Document entity
│       │   ├── query.py            ← Query request/response shapes
│       │   └── request_token.py    ← Trace context model
│       │
│       ├── routes/                 ← Blueprint routing (no logic)
│       │   ├── __init__.py
│       │   ├── page_routes.py      ← /  /results  /tracer  /vocabulary
│       │   └── api_routes.py       ← /api/*
│       │
│       ├── controllers/            ← Orchestration layer
│       │   ├── __init__.py
│       │   ├── search_controller.py   ← VSM, positional, hybrid search
│       │   ├── semantic_controller.py ← Semantic search
│       │   ├── tracer_controller.py   ← Positional intersection tracer
│       │   ├── feedback_controller.py ← Rocchio PRF
│       │   └── vocab_controller.py    ← Vocabulary & postings inspection
│       │
│       └── services/               ← Domain IR engine (framework-agnostic)
│           ├── __init__.py         ← Singleton IR system factory: get_ir_system()
│           ├── preprocessor.py     ← Tokenization, stop-words, Porter Stemmer
│           ├── indexer.py          ← ClothingCorpusIndex (inverted + positional)
│           ├── vsm_service.py      ← lnc.ltc VSM scoring & cosine similarity
│           ├── positional_service.py ← Phrase & ordered proximity search
│           ├── advanced_ir.py      ← Hybrid boost, tracer, Rocchio PRF
│           └── semantic_service.py ← Sentence-transformer semantic search
│
├── frontend/                       ← Client-side Presentation Tier
│   ├── templates/                  ← Jinja2 multi-page templates
│   │   ├── base.html               ← Master layout: nav, footer, modal, core JS
│   │   ├── search.html             ← Home search page
│   │   ├── results.html            ← Ranked results + Rocchio feedback
│   │   ├── tracer.html             ← Positional intersection tracer
│   │   └── index_explorer.html     ← Vocabulary & postings table
│   │
│   └── static/
│       ├── css/
│       │   └── style.css           ← Design system & all component styles
│       └── js/
│           ├── core/               ← Framework primitives
│           │   ├── api-client.js   ← Fetch wrapper with token injection
│           │   ├── app-state.js    ← Reactive state store
│           │   └── router.js       ← Client-side URL manager
│           ├── controllers/        ← Page event handlers & API orchestration
│           │   ├── search.controller.js
│           │   ├── results.controller.js
│           │   ├── tracer.controller.js
│           │   └── vocab.controller.js
│           └── views/              ← Pure DOM rendering (no API calls)
│               ├── search.view.js
│               ├── results.view.js
│               ├── tracer.view.js
│               └── vocab.view.js
│
├── data/
│   └── corpus.txt                  ← Raw corpus: 100 clothing documents (D001–D100)
│
└── output/                         ← Runtime artifacts (auto-generated, gitignored)
    ├── inverted_index.json         ← Serialized inverted index
    ├── positional_index.json       ← Serialized positional index
    ├── semantic_index.pkl          ← Pre-computed sentence embeddings
    └── request_log.jsonl           ← Structured request audit trail
```

---

## 4. Request Flow

```
Browser → Flask Router (Blueprint)
              │
              ▼
         Controller (parse args, orchestrate)
              │
              ▼
         Service (pure IR algorithm)
              │
              ▼
         JSON Response → Frontend Controller → View (DOM render)
```

---

## 5. Coding Standards

1. **Blueprints only route.** Parse parameters and call a controller. Nothing else.
2. **Controllers only orchestrate.** Call services, build response dicts. No SQL, no DOM, no raw math.
3. **Services are pure.** No Flask imports, no `request`, no `g`. Accept plain Python types, return plain Python types.
4. **Views only render.** Frontend `views/*.view.js` files accept data and write HTML. Zero fetch/API calls.
5. **Controllers handle events.** Frontend `controllers/*.controller.js` call the API client and pass data to views.
6. **Deterministic outputs.** Index postings are sorted by `doc_id` for reproducibility.
