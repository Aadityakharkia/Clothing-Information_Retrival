# Clothing Search Engine & Information Retrieval Studio (CSD358)

A high-performance, minimal, and premium Clothing Search Engine and Information Retrieval research platform built on a 100-garment corpus (`D001` - `D100`).

Developed for **CSD358: Information Retrieval Assignment 1**, strictly adhering to all guidelines across **Part A, Part B, Part C, Part D, and Part E**, and featuring **3 Unique Special IR Innovations**.

---

## 🌟 3 Unique Special Information Retrieval Innovations

1. **Innovation 1: Positional-Aware Hybrid Re-Ranking (Dynamic Proximity Boost)**
   - *Theoretical Foundation*: Standard Vector Space Models make the *bag-of-words* assumption, ignoring token distance. Boolean positional queries, on the other hand, are binary and unranked.
   - *Mechanism*: Our hybrid scorer computes standard $lnc.ltc$ cosine similarity, then computes the shortest covering token span $\sigma(d, Q)$ containing matched query terms:
     $$\text{Score}_{\text{hybrid}}(d) = \text{Score}_{\text{VSM}}(d) \times \left(1 + \lambda \cdot \frac{|Q_{\text{matched}}|}{\sigma(d, Q)}\right)$$
   - *Practical Impact*: Clothing descriptions mentioning terms tightly together (e.g. "cotton crew neck t-shirt") receive an immediate rank boost over garments where terms are scattered across 20+ tokens.

2. **Innovation 2: Interactive Postings & Positional Intersection Trace Inspector**
   - *Theoretical Foundation*: Implements and exposes Manning, Raghavan, Schütze (*Introduction to Information Retrieval*, Ch. 2.4) step-by-step positional intersection algorithm.
   - *Mechanism*: Displays live pointer comparisons ($p_1, p_2$), document ID matches, and token distance verifications ($0 < pos_2 - pos_1 \le k$), providing empirical evidence of postings list traversal.

3. **Innovation 3: Vector Space Rocchio Relevance Feedback & Pseudo-Relevance Feedback (PRF)**
   - *Theoretical Foundation*: Adapts the classical vector space Rocchio formula:
     $$\vec{q}_{m} = \alpha \vec{q}_0 + \frac{\beta}{|D_r|} \sum_{d \in D_r} \vec{d} - \frac{\gamma}{|D_{nr}|} \sum_{d \in D_{nr}} \vec{d}$$
   - *Mechanism*: Users can mark retrieved items as relevant or trigger **1-Click Pseudo-Relevance Feedback (PRF)** (top 3 documents). The engine discovers newly boosted clothing attribute terms (e.g., `breathable`, `cotton`, `washable`, `fit`), displays vector drift, and re-ranks the catalog.

---

## 📋 Assignment Specifications & Architecture

### Part A — Corpus & Pre-Processing
- **Corpus**: 100 distinct clothing descriptions (`D001` - `D100`) spanning categories: T-Shirt, Shirt, Jeans, Kurta, Saree, Dress, Hoodie, Jacket, Leggings, Sweatshirt.
- **Tokenization & Normalization**: Punctuation removed via alphanumeric regex; case normalized to lowercase.
- **Stemming**: Custom deterministic implementation of Martin Porter's standard 1980 stemming algorithm (Steps 1a through 5b).
- **Stop-Word Policy & Academic Justification**:
  - High-frequency grammatical function words (*the, is, at, which, on, and, for, it, be, with*) are eliminated.
  - *Justification*: Functional words appear indiscriminately across virtually every clothing product without providing discriminative value between garment types, fabrics, cuts, or styles. Removing them reduces index footprint, speeds up posting traversals, and prevents skewing cosine document lengths.
  - *Consistency*: The exact same pre-processing pipeline and stop-word list are applied identically across document indexing, free-text queries, and positional queries.

### Part B — Vector Space Model (VSM) Ranked Retrieval
- **Weighting Scheme: `lnc.ltc`**:
  - **Document Weight ($lnc$)**:
    $$w_{d,t} = 1 + \log_{10}(tf_{d,t}) \quad (tf > 0, \text{ no } idf)$$
    $$\text{length}(d) = \sqrt{\sum_{t \in d} (w_{d,t})^2}$$
    Normalized weight: $w'_{d,t} = \frac{w_{d,t}}{\text{length}(d)}$
  - **Query Weight ($ltc$)**:
    $$w_{q,t} = (1 + \log_{10}(tf_{q,t})) \times \log_{10}\left(\frac{N}{df_t}\right) \quad (N = 100)$$
    $$\text{length}(q) = \sqrt{\sum_{t \in q} (w_{q,t})^2}$$
    Normalized weight: $w'_{q,t} = \frac{w_{q,t}}{\text{length}(q)}$
  - **Cosine Similarity**:
    $$\text{Score}(q, d) = \sum_{t \in q \cap d} w'_{q,t} \cdot w'_{d,t}$$
- **Ranking**: Sorted by decreasing cosine score; ties broken by increasing `docID`. Returns top-10.

### Part C — Positional Inverted Index
- **Structure**: Every term posting records exact token sequence positions:
  $$\text{term} \rightarrow df \rightarrow [(docID, tf, [p_1, p_2, \dots]), \dots]$$
- **Exact Phrase Search**: Strictly enforces consecutive token positions:
  $$pos(t_{i+1}) = pos(t_i) + 1$$
- **Ordered Proximity Search**: Enforces distance bounds ($WITHIN/k$):
  $$0 < pos(t_2) - pos(t_1) \le k$$

### Part D — Web Application
- Minimalist, high-contrast design inspired by modern showcase interfaces (Image 1 layout) and ultra-bold geometric display typography (Image 2).
- Clean hand-crafted SVG clothing icons for each garment category.
- Live cosine score meters and explicit **Matching Term Positions** evidence displayed on each card.
- 4 interactive views: Search Engine, Positional Tracer, Test Suite Dashboard, and Index Explorer.

### Part E — Mandatory Tests & Deliverables
All mandatory tests are automated in `src/test_runner.py`:
- 10 free-text queries (including Out-Of-Vocabulary query: `waterproof cyberpunk rainwear`).
- 5 exact phrase queries (`"cotton shirt"`, `"stretch denim"`, `"festive wear"`, `"winter wear"`, `"regular fit"`).
- 4 proximity queries with varying $k$ (`cotton WITHIN/3 shirt`, `stretch WITHIN/4 denim`, `winter WITHIN/3 wear`, `festive WITHIN/4 kurta`).
- Detailed comparative analysis explaining why positional information changes the result set and order.

---

## 📁 Repository Structure

```
Clothing-Information_Retrival/
├── data/
│   └── corpus.txt                          # 100-document clothing corpus (D001-D100)
├── output/
│   ├── inverted_index.txt                  # Human-readable dictionary/inverted index
│   ├── inverted_index.json                 # Machine-readable inverted index
│   ├── positional_index.txt                # Human-readable positional index
│   ├── positional_index.json               # Machine-readable positional index
│   ├── test_results_report.md              # Complete Part E mandatory test report
│   └── test_results_report.json            # JSON benchmark outputs
├── src/
│   ├── __init__.py
│   ├── preprocessor.py                     # Case folding, Porter Stemmer, stop-words
│   ├── indexer.py                          # Inverted and Positional Index builder
│   ├── vsm.py                              # lnc.ltc Vector Space Model retriever
│   ├── positional_search.py                # Exact phrase and WITHIN/k proximity
│   ├── advanced_ir.py                      # 3 Special Ideas (Hybrid Boost, Trace, Rocchio)
│   └── test_runner.py                      # Automated test suite runner
├── web/
│   ├── app.py                              # Flask REST API and web server
│   ├── templates/
│   │   └── index.html                      # Minimal & premium clothing search UI
│   └── static/
│       ├── css/style.css                   # Bespoke stylesheet (Image 1 + Image 2)
│       └── js/app.js                       # Frontend search, PRF, tracer, and modal logic
├── tests/
│   └── test_ir_engine.py                   # Pytest test suite (10/10 tests pass)
├── export_deliverables.py                  # Generates outputs & creates submission ZIP
├── pytest.ini                              # Test configuration
└── README.md                               # Project documentation
```

---

## 🚀 How to Run Locally

### 1. Run Automated Tests
```bash
pytest -v
```
All 10 unit tests pass, verifying stemming, index consistency, `lnc.ltc` cosine scoring, phrase matching, proximity constraints, and out-of-vocabulary handling.

### 2. Export Deliverables & Submission ZIP
```bash
python export_deliverables.py
```
This generates all index outputs (`output/inverted_index.txt`, `output/positional_index.txt`, etc.), executes the test suite, and bundles everything into:
`CSD358_Assignment1_Clothing_Search_Engine.zip`.

### 3. Launch the Web Application
```bash
python web/app.py
```
Open your browser and navigate to:
**`http://127.0.0.1:5000`**

---

## 🔬 Comparative Analysis: Positional vs VSM (Part E)

### Case 1: Pure VSM vs Exact Phrase (`"cotton shirt"`)
- **VSM Behavior**: In bag-of-words VSM, `D001` (T-shirt) receives high cosine similarity because "cotton" and "shirt" both occur inside the text, even though "cotton" refers to fabric and "shirt" is part of the t-shirt title.
- **Positional Behavior**: Exact phrase search strictly enforces $pos(\text{shirt}) = pos(\text{cotton}) + 1$. It rejects `D001` and retrieves only genuine shirts (`D002, D022, D042, D062, D082`), demonstrating how positional information eliminates false-positive co-occurrences.

### Case 2: Broad Co-occurrence vs Proximity (`winter WITHIN/3 wear`)
- **VSM Behavior**: The word "wear" is ubiquitous in the corpus ("everyday Indian wear", "daily wear"). In pure VSM, dozens of sarees, kurtas, and dresses obtain non-zero cosine scores simply due to matching "wear".
- **Positional Behavior**: Proximity search with $k=3$ requires "wear" to occur within 3 tokens after "winter". This correctly isolates authentic winter wear (Jackets, Hoodies, Sweatshirts) and excludes unrelated garments.

### Case 3: Positional Hybrid Proximity Re-Ranking (Special Idea 1)
- When Proximity Boost is toggled on, garments where terms occur in an immediate 2-token span receive up to a 50% score boost, re-ranking them directly based on physical token proximity in the text.