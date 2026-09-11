# Clothing Information Retrieval Engine
### CSD358 — Information Retrieval · Assignment 1

A full-stack Information Retrieval research platform implementing classic and advanced IR algorithms on a 100-document clothing corpus.

---

## First-Time Setup & Running

### Prerequisites
- **Python 3.9+**
- **Node.js** *(optional, provides convenient npm scripts)*

---

### Option A: Using NPM (Recommended)

```bash
# 1. First-time setup: creates a virtual environment (.venv) and installs all dependencies
npm run setup

# 2. Start the development server
npm run dev
```

---

### Option B: Manual Setup (Pure Python)

> [!IMPORTANT]
> Modern macOS (Homebrew) and Linux environments enforce [PEP 668](https://peps.python.org/pep-0668/) (*externally-managed-environment*). Always use a virtual environment rather than global `pip` to avoid installation errors.

```bash
# Step 1: Create a virtual environment
python3 -m venv .venv

# Step 2: Activate the virtual environment
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate       # Windows (Command Prompt / PowerShell)

# Step 3: Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Step 4: Run the server
python backend/server.py
```

---

### Accessing the Web Application

Once running, open your browser and visit:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

### What to Expect on First Run
1. **Dependency Download**: Installing dependencies via `requirements.txt` downloads PyTorch and Sentence-Transformers (~1–2 minutes depending on network speed).
2. **Automatic Index Generation**: On first launch, the backend reads [data/corpus.json](file:///Users/aaditya/Library/Mobile%20Documents/com~apple~CloudDocs/Downloads/SNU/SEM%205/IR/Assignment/Clothing-Information_Retrival/data/corpus.json) and compiles:
   - Inverted Index (`output/inverted_index.json`)
   - Positional Index (`output/positional_index.json`)
   - Semantic Embeddings (`output/semantic_index.pkl`)
3. **Subsequent Boots**: Load cached indices from `output/` instantly without rebuilding.

---

### Troubleshooting Common Issues

| Issue | Cause | Fix |
|---|---|---|
| `error: externally-managed-environment` | Installing packages globally on macOS / Homebrew Python | Run `python3 -m venv .venv` and install inside the active `.venv` (or use `npm run setup`) |
| `ModuleNotFoundError: No module named 'flask'` | Server executed using global python instead of virtual environment | Run with `.venv/bin/python3 backend/server.py` or activate venv (`source .venv/bin/activate`) |
| `Address already in use (port 5000)` | Another process is occupying port 5000 (e.g., macOS AirPlay Receiver) | Free the port with `lsof -ti :5000 \| xargs kill -9` or disable AirPlay Receiver in macOS System Settings > General > AirDrop & Handoff |

---

## Pages

| Route | Description |
|---|---|
| `/` | Search home — enter queries, choose search mode |
| `/results?q=<query>&mode=<mode>` | Ranked results with document inspection |
| `/tracer` | Positional intersection step-by-step tracer |
| `/vocabulary` | Inverted index explorer — browse all terms & postings |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Server health check |
| GET | `/api/search/vsm?q=<query>` | VSM lnc.ltc ranked retrieval |
| GET | `/api/search/positional?q=<query>` | Phrase / proximity search |
| GET | `/api/search/hybrid?q=<query>` | VSM + proximity boost |
| GET | `/api/search/semantic?q=<query>` | Sentence-transformer semantic search |
| GET | `/api/trace?term1=<t1>&term2=<t2>&k=<k>` | Positional intersection trace |
| POST | `/api/feedback` | Rocchio relevance feedback / PRF |
| GET | `/api/vocabulary?search=<term>` | Browse vocabulary & postings |
| GET | `/api/doc/<doc_id>` | Full document details + token map |

---

## Search Modes

| Mode | Algorithm |
|---|---|
| **VSM** | lnc.ltc Vector Space Model with Porter Stemmer |
| **Phrase** | Exact phrase matching via positional index |
| **Proximity** | Ordered term proximity within *k* positions |
| **Semantic** | Sentence-transformers + optional hybrid with VSM |

---

## npm Scripts

| Command | Action |
|---|---|
| `npm run dev` | Start Flask in development mode (debug on, auto-reload) |
| `npm start` | Start Flask in production mode |
| `npm run setup` | Install all Python dependencies |

---

## Project Structure

```
Clothing-Information_Retrival/
├── package.json          ← npm run dev / start / setup
├── requirements.txt      ← Python dependencies
│
├── backend/              ← Server-side Python (Flask)
│   ├── server.py         ← Entry point
│   ├── config.py         ← Dev/Prod configuration
│   └── app/
│       ├── middleware/   ← Request tracking, error handling
│       ├── models/       ← Document, Query, RequestTrace
│       ├── routes/       ← Flask Blueprints (routing only)
│       ├── controllers/  ← Orchestration layer
│       └── services/     ← IR algorithms (VSM, Positional, Semantic…)
│
├── frontend/             ← Client-side (Jinja2 + CSS + JS)
│   ├── templates/        ← HTML page templates
│   └── static/
│       ├── css/          ← Styling
│       └── js/
│           ├── core/     ← API client, router, app state
│           ├── controllers/  ← Page controllers
│           └── views/    ← DOM rendering layers
│
├── data/
│   └── corpus.txt        ← 100 clothing product documents
│
└── output/               ← Runtime artifacts (auto-generated)
    ├── inverted_index.json
    ├── positional_index.json
    ├── semantic_index.pkl
    └── request_log.jsonl
```

---

## IR Algorithms Implemented

- **Tokenization & Preprocessing** — case folding, stop-word removal, Porter Stemmer
- **Inverted Index** — dictionary with postings list (df, tf per doc)
- **Positional Index** — token positions for phrase & proximity queries
- **VSM (lnc.ltc)** — logarithmic TF + IDF weighting, cosine similarity
- **Phrase Search** — exact ordered token sequence via positional lists
- **Proximity Search** — WITHIN/k ordered proximity verification
- **Hybrid Proximity Boost** — VSM score × proximity bonus (λ-weighted)
- **Semantic Search** — sentence-transformers embeddings (all-MiniLM-L6-v2)
- **Rocchio PRF** — relevance feedback with pseudo-relevant document expansion
- **Positional Tracer** — step-by-step positional intersection visualization