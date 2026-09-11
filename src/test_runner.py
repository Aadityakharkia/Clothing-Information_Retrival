"""
Mandatory Assignment Test Runner (CSD358 Part E)
================================================
Executes and documents all mandatory assignment tests:
1. At least 10 free-text queries (VSM lnc.ltc).
2. At least 5 exact phrase queries (Positional Index).
3. At least 3 proximity queries with different values of k (Positional Index).
4. At least one query containing an Out-Of-Vocabulary (OOV) term.
5. In-depth comparative analysis of at least 2 cases where positional information
   changes the result set or order compared to ordinary VSM bag-of-words retrieval.
"""

import os
import json
from typing import Dict, List, Any
from .indexer import ClothingCorpusIndex
from .vsm import VSMRetriever
from .positional_search import PositionalSearcher
from .advanced_ir import AdvancedIREngine


# 10 Free-Text Queries (including out-of-vocabulary query)
FREE_TEXT_QUERIES = [
    "breathable cotton t-shirt",
    "black slim fit casual shirt",
    "stretch denim jeans grey",
    "festive wear saree printed border",
    "women winter warm fleece hoodie",
    "comfortable kurta everyday Indian wear",
    "quilted puffer jacket lightweight",
    "high waist stretch leggings olive",
    "casual fit dress minimal shrinkage",
    "waterproof cyberpunk rainwear"  # Out-Of-Vocabulary (OOV) query: terms not in corpus!
]

# 5 Exact Phrase Queries
EXACT_PHRASE_QUERIES = [
    '"cotton shirt"',
    '"stretch denim"',
    '"festive wear"',
    '"winter wear"',
    '"regular fit"'
]

# 3 Proximity Queries with different values of k
PROXIMITY_QUERIES = [
    ("cotton WITHIN/3 shirt", "cotton", "shirt", 3),
    ("stretch WITHIN/4 denim", "stretch", "denim", 4),
    ("winter WITHIN/3 wear", "winter", "wear", 3),
    ("festive WITHIN/4 kurta", "festive", "kurta", 4)
]


class TestRunner:
    """Automates execution and report generation for Assignment Part E."""

    def __init__(self, corpus_path: str, output_dir: str):
        self.corpus_path = corpus_path
        self.output_dir = output_dir
        self.index = ClothingCorpusIndex(corpus_path)
        self.vsm = VSMRetriever(self.index)
        self.positional = PositionalSearcher(self.index)
        self.advanced = AdvancedIREngine(self.index, self.vsm)

    def run_all_tests(self) -> Dict[str, Any]:
        """Runs all mandatory query tests and formats the results."""
        os.makedirs(self.output_dir, exist_ok=True)
        # Save indices first
        self.index.save_indices(self.output_dir)

        results = {
            "free_text_tests": [],
            "exact_phrase_tests": [],
            "proximity_tests": [],
            "comparative_analysis": []
        }

        # 1. Run 10 Free-Text Queries
        for q in FREE_TEXT_QUERIES:
            vsm_res = self.vsm.search(q, top_k=10)
            norm_w, q_len, q_det = self.vsm.compute_query_weights(q)
            results["free_text_tests"].append({
                "query": q,
                "query_length": round(q_len, 4),
                "terms_analyzed": q_det,
                "top_10_results": [
                    {
                        "rank": r["rank"],
                        "doc_id": r["doc_id"],
                        "category": r["category"],
                        "title": r["title"],
                        "cosine_score": r["cosine_score"]
                    }
                    for r in vsm_res
                ]
            })

        # 2. Run 5 Exact Phrase Queries
        for phrase in EXACT_PHRASE_QUERIES:
            phrase_res = self.positional.search_exact_phrase(phrase)
            results["exact_phrase_tests"].append({
                "query": phrase,
                "total_matches": len(phrase_res),
                "results": [
                    {
                        "doc_id": r["doc_id"],
                        "category": r["category"],
                        "title": r["title"],
                        "match_count": r["match_count"],
                        "matched_positions": r["matched_positions"]
                    }
                    for r in phrase_res[:10]
                ]
            })

        # 3. Run Proximity Queries
        for raw_q, t1, t2, k in PROXIMITY_QUERIES:
            prox_res = self.positional.search_proximity(t1, t2, k)
            results["proximity_tests"].append({
                "query": raw_q,
                "term1": t1,
                "term2": t2,
                "k": k,
                "total_matches": len(prox_res),
                "results": [
                    {
                        "doc_id": r["doc_id"],
                        "category": r["category"],
                        "title": r["title"],
                        "match_count": r["match_count"],
                        "matched_pairs": r["matched_pairs"]
                    }
                    for r in prox_res[:10]
                ]
            })

        # 4. Comparative Analysis: Cases where positional information changes result set / order
        # Case 1: "cotton shirt" (VSM Bag-of-Words vs Exact Phrase)
        vsm_cotton_shirt = self.vsm.search("cotton shirt", top_k=10)
        phrase_cotton_shirt = self.positional.search_exact_phrase("cotton shirt")
        phrase_cotton_shirt_docs = {r["doc_id"] for r in phrase_cotton_shirt}

        # Case 2: "winter wear" vs "winter WITHIN/3 wear"
        vsm_winter_wear = self.vsm.search("winter wear", top_k=10)
        prox_winter_wear = self.positional.search_proximity("winter", "wear", 3)
        prox_winter_wear_docs = {r["doc_id"] for r in prox_winter_wear}

        # Case 3: Positional Hybrid Boost comparison on "stretch denim"
        hybrid_stretch_denim = self.advanced.search_hybrid_proximity_boost("stretch denim", lambda_param=0.5, top_k=10)

        results["comparative_analysis"] = {
            "case_1_cotton_shirt": {
                "description": "Comparison between Free-Text VSM bag-of-words and Exact Phrase for 'cotton shirt'",
                "vsm_top_10": [r["doc_id"] for r in vsm_cotton_shirt],
                "phrase_docs": list(phrase_cotton_shirt_docs),
                "explanation": (
                    "In pure VSM retrieval for 'cotton shirt', documents containing 'cotton' and 'shirt' "
                    "at distant positions (for instance, D001, D011 where 'cotton' describes fabric and 'shirt' appears in t-shirt) "
                    "receive high cosine scores due to bag-of-words term frequency. In contrast, Positional Exact Phrase retrieval "
                    "strictly enforces pos(shirt) == pos(cotton) + 1, filtering out documents where the two terms do not occur "
                    "as an uninterrupted phrase. For example, D002, D022, D042, D062, D082 ('Men's Checked Cotton Shirt') match the exact phrase, "
                    "whereas documents mentioning both words in separate contexts are properly excluded."
                )
            },
            "case_2_winter_wear": {
                "description": "Comparison between Free-Text VSM and Proximity Search 'winter WITHIN/3 wear'",
                "vsm_top_10": [r["doc_id"] for r in vsm_winter_wear],
                "proximity_docs": list(prox_winter_wear_docs),
                "explanation": (
                    "In VSM retrieval for 'winter wear', every document mentioning either 'winter' or 'wear' "
                    "is retrieved. Because 'wear' is ubiquitous in the clothing corpus ('everyday Indian wear', 'daily wear', etc.), "
                    "numerous documents (e.g. Sarees, Kurtas) obtain non-zero cosine similarity even if they have no winter association. "
                    "Positional proximity search with k=3 requires 'wear' to appear within 3 tokens after 'winter', isolating genuine "
                    "winter apparel mentions ('winter wear' in Jackets, Hoodies, Sweatshirts) and discarding false-positive co-occurrences."
                )
            },
            "case_3_hybrid_rerank": {
                "description": "Positional Hybrid Proximity Boost re-ordering",
                "results": [
                    {"doc_id": r["doc_id"], "vsm_score": r["vsm_score"], "hybrid_score": r["hybrid_score"], "span": r["shortest_span"]}
                    for r in hybrid_stretch_denim[:5]
                ],
                "explanation": (
                    "When applying our Positional Hybrid Proximity Boost (Special Idea 1), documents having terms in an immediate 2-token span "
                    "receive an elevated boost over documents where terms are separated by filler words, demonstrating ranked re-ordering "
                    "driven directly by positional token distance."
                )
            }
        }

        # Save JSON output
        report_json_path = os.path.join(self.output_dir, "test_results_report.json")
        with open(report_json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        # Generate Markdown Report
        self._write_markdown_report(results)

        return results

    def _write_markdown_report(self, results: Dict[str, Any]):
        """Formats comprehensive human-readable Markdown test report."""
        report_md_path = os.path.join(self.output_dir, "test_results_report.md")
        with open(report_md_path, "w", encoding="utf-8") as f:
            f.write("# Information Retrieval Assignment-1 (CSD358) - Comprehensive Test Report\n\n")
            f.write("**Corpus Size**: 100 Documents (D001 - D100)\n")
            f.write("**Weighting Scheme**: Vector Space Model `lnc.ltc` with Cosine Normalization\n")
            f.write("**Positional Indexing**: Exact Phrase (`k=1`) & Ordered Proximity (`WITHIN/k`)\n\n")
            f.write("---\n\n")

            # Part 1: Free Text Queries
            f.write("## 1. Free-Text Queries (VSM `lnc.ltc`)\n\n")
            for i, test in enumerate(results["free_text_tests"], start=1):
                f.write(f"### Query {i}: `{test['query']}`\n\n")
                if "waterproof" in test["query"]:
                    f.write("> **Out-of-Vocabulary (OOV) Test Case**: Notice that words like 'cyberpunk' and 'rainwear' do not appear in the corpus. The system safely returns empty results or zero scores without throwing exceptions.\n\n")
                f.write("| Rank | Doc ID | Category | Product Title | Cosine Score |\n")
                f.write("|:---:|:---:|:---:|:---|:---:|\n")
                if not test["top_10_results"]:
                    f.write("| - | *No matching documents* | - | Query terms Out-Of-Vocabulary | 0.0000 |\n")
                else:
                    for r in test["top_10_results"]:
                        f.write(f"| {r['rank']} | **{r['doc_id']}** | {r['category']} | {r['title']} | `{r['cosine_score']:.6f}` |\n")
                f.write("\n")

            # Part 2: Exact Phrase Queries
            f.write("## 2. Exact Phrase Queries (Positional Index)\n\n")
            for i, test in enumerate(results["exact_phrase_tests"], start=1):
                f.write(f"### Phrase Query {i}: `{test['query']}` (Total Matches: {test['total_matches']})\n\n")
                f.write("| Doc ID | Category | Product Title | Matches | Matched Positions `[p1, p2, ...]` |\n")
                f.write("|:---:|:---:|:---|:---:|:---|\n")
                if not test["results"]:
                    f.write("| - | - | *No exact phrase matches found* | 0 | - |\n")
                else:
                    for r in test["results"]:
                        f.write(f"| **{r['doc_id']}** | {r['category']} | {r['title']} | {r['match_count']} | `{r['matched_positions']}` |\n")
                f.write("\n")

            # Part 3: Proximity Queries
            f.write("## 3. Ordered Proximity Queries (`term1 WITHIN/k term2`)\n\n")
            for i, test in enumerate(results["proximity_tests"], start=1):
                f.write(f"### Proximity Query {i}: `{test['query']}` (k={test['k']}, Total Matches: {test['total_matches']})\n\n")
                f.write("| Doc ID | Category | Product Title | Matches | Position Pairs `(pos1, pos2, dist)` |\n")
                f.write("|:---:|:---:|:---|:---:|:---|\n")
                for r in test["results"][:8]:
                    pairs_str = ", ".join([f"({p[0]}, {p[1]}, d={p[2]})" for p in r["matched_pairs"]])
                    f.write(f"| **{r['doc_id']}** | {r['category']} | {r['title']} | {r['match_count']} | `{pairs_str}` |\n")
                f.write("\n")

            # Part 4: Comparative Analysis
            f.write("## 4. In-Depth Comparative Analysis (Positional vs VSM)\n\n")
            ca = results["comparative_analysis"]

            f.write("### Case 1: Pure VSM vs Exact Phrase (`\"cotton shirt\"`)\n\n")
            f.write(f"{ca['case_1_cotton_shirt']['explanation']}\n\n")
            f.write(f"- **VSM Top 5 DocIDs**: `{ca['case_1_cotton_shirt']['vsm_top_10'][:5]}`\n")
            f.write(f"- **Exact Phrase DocIDs**: `{sorted(ca['case_1_cotton_shirt']['phrase_docs'])[:10]}`\n\n")

            f.write("### Case 2: Broad Co-occurrence vs Proximity (`winter WITHIN/3 wear`)\n\n")
            f.write(f"{ca['case_2_winter_wear']['explanation']}\n\n")
            f.write(f"- **VSM Top 5 DocIDs**: `{ca['case_2_winter_wear']['vsm_top_10'][:5]}`\n")
            f.write(f"- **Proximity DocIDs**: `{sorted(ca['case_2_winter_wear']['proximity_docs'])[:10]}`\n\n")

            f.write("### Case 3: Positional Hybrid Proximity Re-Ranking (Special Idea 1)\n\n")
            f.write(f"{ca['case_3_hybrid_rerank']['explanation']}\n\n")
            f.write("| Doc ID | Base VSM Score | Shortest Span (tokens) | Hybrid Proximity Score |\n")
            f.write("|:---:|:---:|:---:|:---:|\n")
            for item in ca["case_3_hybrid_rerank"]["results"]:
                f.write(f"| **{item['doc_id']}** | `{item['vsm_score']:.6f}` | `{item['span']}` | `{item['hybrid_score']:.6f}` |\n")
            f.write("\n")
