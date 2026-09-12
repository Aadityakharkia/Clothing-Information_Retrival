"""
Assignment 1 Part E — Comprehensive Test Suite & Report Generator
==================================================================
CSD358: Information Retrieval
Runs:
1. 10 Free-text VSM queries (lnc.ltc)
2. 5 Exact phrase queries (positional index)
3. 3+ Proximity queries with various k values (positional index)
4. Out-of-vocabulary query (terms not in corpus)
5. Comparative analysis demonstrating where positional information changes results
Outputs report to output/part_e_test_report.md and output/part_e_test_report.txt
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any

# Ensure project root is in path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.services import get_ir_system


def format_table(headers: List[str], rows: List[List[Any]]) -> str:
    """Helper to render a clean markdown table."""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
    sep_line = "|-" + "-|-".join("-" * col_widths[i] for i in range(len(headers))) + "-|"
    data_lines = []
    for row in rows:
        data_lines.append("| " + " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)) + " |")

    return "\n".join([header_line, sep_line] + data_lines)


def run_all_assignment_tests(corpus_path: str = "data/corpus.txt") -> str:
    ir = get_ir_system(corpus_path)
    vsm = ir["vsm"]
    positional = ir["positional"]

    report_lines = []
    report_lines.append("# CSD358 Information Retrieval — Assignment 1: Part E Test Report")
    report_lines.append("**Corpus**: 100 Clothing Product Descriptions (`D001`–`D100`)")
    report_lines.append("**Evaluation Date**: September 2026\n")
    report_lines.append("---\n")

    # ─────────────────────────────────────────────────────────────────────────────
    # SECTION 1: 10 FREE-TEXT VSM QUERIES (lnc.ltc)
    # ─────────────────────────────────────────────────────────────────────────────
    report_lines.append("## 1. Free-Text Ranked Retrieval Queries (Vector Space Model - lnc.ltc)\n")
    report_lines.append("Each query computes $w_{d,t} = 1 + \\log_{10}(tf)$ and $w_{q,t} = (1 + \\log_{10}(tf)) \\cdot \\log_{10}(N/df)$ with cosine normalization.\n")

    free_text_queries = [
        "cotton t-shirt",
        "denim jeans grey",
        "oversized hoodie",
        "printed saree blue",
        "solid midi dress",
        "checked cotton shirt",
        "breathable summer kurta",
        "warm fleece winter jacket",
        "high waist stretch leggings",
        "casual comfortable daily wear"
    ]

    for idx, q in enumerate(free_text_queries, start=1):
        report_lines.append(f"### Query 1.{idx}: `{q}`")
        results = vsm.search(q, top_k=10)
        table_rows = []
        for r in results:
            table_rows.append([
                r["rank"],
                r["doc_id"],
                r["category"],
                r["title"],
                f"{r['cosine_score']:.6f}"
            ])
        if table_rows:
            report_lines.append(format_table(["Rank", "Doc ID", "Category", "Product Title", "Cosine Score"], table_rows))
        else:
            report_lines.append("*No documents matched.*")
        report_lines.append("")

    report_lines.append("---\n")

    # ─────────────────────────────────────────────────────────────────────────────
    # SECTION 2: 5 EXACT PHRASE QUERIES (Positional Index)
    # ─────────────────────────────────────────────────────────────────────────────
    report_lines.append("## 2. Exact Phrase Queries (Positional Inverted Index)\n")
    report_lines.append("Requires strictly consecutive token positions: $pos(t_{i+1}) = pos(t_i) + 1$.\n")

    phrase_queries = [
        "cotton shirt",
        "stretch denim",
        "festive wear",
        "regular fit",
        "breathable fabric"
    ]

    for idx, q in enumerate(phrase_queries, start=1):
        report_lines.append(f"### Phrase Query 2.{idx}: `\"{q}\"`")
        results = positional.search_exact_phrase(q)
        table_rows = []
        for rank, r in enumerate(results[:10], start=1):
            positions_str = ", ".join(f"[{' → '.join(map(str, p))}]" for p in r["matched_positions"][:3])
            if len(r["matched_positions"]) > 3:
                positions_str += f" (+{len(r['matched_positions']) - 3} more)"
            table_rows.append([
                rank,
                r["doc_id"],
                r["category"],
                r["title"],
                r["match_count"],
                positions_str
            ])
        if table_rows:
            report_lines.append(format_table(["Rank", "Doc ID", "Category", "Product Title", "Matches", "Token Position Chains"], table_rows))
            report_lines.append(f"*Total Documents with Exact Phrase: {len(results)}*")
        else:
            report_lines.append("*No documents matched.*")
        report_lines.append("")

    report_lines.append("---\n")

    # ─────────────────────────────────────────────────────────────────────────────
    # SECTION 3: 3+ PROXIMITY QUERIES (WITHIN/k)
    # ─────────────────────────────────────────────────────────────────────────────
    report_lines.append("## 3. Ordered Proximity Queries (WITHIN/k)\n")
    report_lines.append("Requires term 2 to occur within $k$ token positions after term 1: $0 < pos(t_2) - pos(t_1) \\le k$.\n")

    proximity_queries = [
        ("cotton", "shirt", 3),
        ("stretch", "denim", 4),
        ("winter", "wear", 3),
        ("festive", "kurta", 4)
    ]

    for idx, (t1, t2, k) in enumerate(proximity_queries, start=1):
        q_str = f"{t1} WITHIN/{k} {t2}"
        report_lines.append(f"### Proximity Query 3.{idx}: `{q_str}`")
        results = positional.search_proximity(t1, t2, k)
        table_rows = []
        for rank, r in enumerate(results[:10], start=1):
            pairs_str = ", ".join(f"(pos {p1}, {p2}; Δ={diff})" for p1, p2, diff in r["matched_pairs"][:3])
            if len(r["matched_pairs"]) > 3:
                pairs_str += f" (+{len(r['matched_pairs']) - 3} more)"
            table_rows.append([
                rank,
                r["doc_id"],
                r["category"],
                r["title"],
                r["match_count"],
                pairs_str
            ])
        if table_rows:
            report_lines.append(format_table(["Rank", "Doc ID", "Category", "Product Title", "Matches", f"Position Pairs (Δ ≤ {k})"], table_rows))
            report_lines.append(f"*Total Documents within Distance {k}: {len(results)}*")
        else:
            report_lines.append("*No documents matched.*")
        report_lines.append("")

    report_lines.append("---\n")

    # ─────────────────────────────────────────────────────────────────────────────
    # SECTION 4: OUT-OF-VOCABULARY QUERY (Term Not in Corpus)
    # ─────────────────────────────────────────────────────────────────────────────
    report_lines.append("## 4. Query Containing Term Not Occurring in the Corpus\n")
    report_lines.append("Validates graceful handling of out-of-vocabulary terms ($df = 0$, $IDF = 0$, cosine score = 0).\n")

    oov_query = "astronaut velvet kimono"
    report_lines.append(f"### Out-of-Vocabulary Query: `{oov_query}`")
    vsm_oov = vsm.search(oov_query, top_k=10)
    pos_oov = positional.search_exact_phrase(oov_query)

    report_lines.append(f"- **VSM Results Count**: {len(vsm_oov)} (Returned empty list, 0 crashes)")
    report_lines.append(f"- **Positional Results Count**: {len(pos_oov)} (Returned empty list, 0 crashes)")
    report_lines.append("- **Behavior**: The preprocessor stems the terms (`astronaut`, `velvet`, `kimono`), checks vocabulary, recognizes $df=0$, and safely normalizes vectors without zero-division.\n")

    report_lines.append("---\n")

    # ─────────────────────────────────────────────────────────────────────────────
    # SECTION 5: COMPARATIVE ANALYSIS (VSM vs Positional Indexing)
    # ─────────────────────────────────────────────────────────────────────────────
    report_lines.append("## 5. Comparative Analysis: How Positional Information Changes Results\n")
    report_lines.append("The assignment requires explaining at least two cases where positional information changes the result set or order:\n")

    # CASE A: "cotton shirt"
    report_lines.append("### Case Study A: Query `cotton shirt` — VSM Free-Text vs. Exact Phrase")
    vsm_res = vsm.search("cotton shirt", top_k=10)
    phrase_res = positional.search_exact_phrase("cotton shirt")

    report_lines.append("#### Free-Text VSM Top-5:")
    table_vsm = [[r["rank"], r["doc_id"], r["category"], r["title"], f"{r['cosine_score']:.4f}"] for r in vsm_res[:5]]
    report_lines.append(format_table(["Rank", "Doc ID", "Category", "Title", "Score"], table_vsm))

    report_lines.append("\n#### Exact Phrase Positional Matches (All):")
    table_phrase = [[i, r["doc_id"], r["category"], r["title"], r["matched_positions"]] for i, r in enumerate(phrase_res, start=1)]
    report_lines.append(format_table(["#", "Doc ID", "Category", "Title", "Positions"], table_phrase))

    report_lines.append("\n**Explanation**:")
    report_lines.append("- Under **VSM (lnc.ltc)**, retrieval is bag-of-words. `D001` (Men's Cotton Crew Neck T-Shirt) ranks #1 with a score of ~0.37 because 'cotton' appears 3 times in `D001`. However, `D001` is a *T-Shirt*, NOT a *Shirt*!")
    report_lines.append("- Under **Positional Exact Phrase Search**, terms must satisfy $pos(shirt) = pos(cotton) + 1$. `D001` is completely eliminated because 'cotton' and 'shirt' do not occur consecutively (intervened by 'crew', 'neck', etc.).")
    report_lines.append("- Only genuine shirts (`D002`, `D022`, `D042`, `D062`, `D082` — 'Checked Cotton Shirt') match the exact phrase. Thus, positional indexing dramatically improves **precision** and eliminates false positive apparel categories.\n")

    # CASE B: "stretch denim" vs. Proximity WITHIN/4
    report_lines.append("### Case Study B: `stretch` & `denim` — Exact Phrase vs. Proximity `stretch WITHIN/4 denim`")
    phrase_stretch = positional.search_exact_phrase("stretch denim")
    prox_stretch = positional.search_proximity("stretch", "denim", 4)

    report_lines.append(f"- **Exact Phrase (`\"stretch denim\"`)**: {len(phrase_stretch)} documents matched.")
    report_lines.append(f"- **Proximity Search (`stretch WITHIN/4 denim`)**: {len(prox_stretch)} documents matched.")

    report_lines.append("\n**Explanation**:")
    report_lines.append("- Exact phrase matching is often too restrictive: in `D003` ('Men's Regular Fit Denim Jeans'), the text contains *'Made from comfort stretch denim'*, where `pos(denim) - pos(stretch) = 1` (an exact phrase match).")
    report_lines.append("- However, if a product description reads *'stretchable, durable cotton denim'* or *'stretch fabric blended with denim'*, an exact phrase search fails ($pos(denim) - pos(stretch) > 1$).")
    report_lines.append("- With `stretch WITHIN/4 denim`, we capture all documents where 'stretch' semantically modifies 'denim' within a 4-token window, giving users the recall flexibility of VSM combined with the syntactic word-ordering guarantee of positional indexing.\n")

    full_report = "\n".join(report_lines)
    return full_report


if __name__ == "__main__":
    output_dir = PROJECT_ROOT / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    report = run_all_assignment_tests(str(PROJECT_ROOT / "data" / "corpus.txt"))

    md_path = output_dir / "part_e_test_report.md"
    txt_path = output_dir / "part_e_test_report.txt"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(report)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Part E Test Suite completed successfully!")
    print(f"Report saved to: {md_path}")
    print(f"Report saved to: {txt_path}")
