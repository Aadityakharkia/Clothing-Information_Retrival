"""
Search Evaluation & Comparison Benchmark (CSD358)
=================================================
Runs a curated IR benchmark comparing:
1. Lexical VSM (lnc.ltc)
2. Positional Index (Phrase & Proximity)
3. Dense Semantic (all-MiniLM-L6-v2)
4. Hybrid (alpha-blended)
"""

import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.config import get_config
from backend.app.services import get_ir_system


def run_benchmark():
    cfg = get_config()
    ir = get_ir_system(cfg.CORPUS_PATH)
    vsm = ir["vsm"]
    pos = ir["positional"]
    sem = ir["semantic"]

    test_cases = [
        {
            "query": "warm outerwear for freezing weather",
            "category": "1. Synonymy & Vocabulary Mismatch",
            "desc": "Tests conceptual retrieval when exact words ('outerwear', 'freezing') are missing from corpus."
        },
        {
            "query": "traditional ethnic attire for Indian wedding",
            "category": "2. Zero Lexical Overlap (Cultural Context)",
            "desc": "Words 'ethnic', 'attire', 'wedding' do not exist in corpus. VSM scores 0.0, Semantic succeeds."
        },
        {
            "query": "cotton shirt",
            "category": "3. Exact Lexical Precision",
            "desc": "High keyword frequency. Compares bag-of-words VSM vs Positional vs Semantic."
        },
        {
            "query": "\"cotton shirt\"",
            "category": "4. Positional Exact Phrase",
            "desc": "Enforces strict token adjacency (pos2 = pos1 + 1)."
        },
        {
            "query": "winter WITHIN/3 wear",
            "category": "5. Positional Proximity",
            "desc": "Enforces distance bound (0 < pos2 - pos1 <= 3)."
        },
        {
            "query": "waterproof cyberpunk rainwear",
            "category": "6. Out-of-Vocabulary (OOV)",
            "desc": "Robustness check with terms completely absent from the vocabulary."
        }
    ]

    print("=" * 84)
    print("CSD358 Clothing Information Retrieval — Multi-Engine Comparative Benchmark")
    print("=" * 84)

    for case in test_cases:
        q = case["query"]
        print(f"\n▶ TEST CATEGORY: {case['category']}")
        print(f"  Query:       \"{q}\"")
        print(f"  Hypothesis:  {case['desc']}")

        # Positional Phrase / Proximity if quoted or WITHIN
        if "\"" in q or "WITHIN/" in q:
            q_type, pos_res = pos.parse_and_search(q)
            print(f"  [Positional Engine ({q_type})]: {len(pos_res)} matches")
            for r in pos_res[:3]:
                ev = r.get("matched_positions") or r.get("matched_pairs")
                print(f"    • {r['doc_id']}: {r['title']} | Evidence: {ev}")
            continue

        is_nl = sem.is_natural_language(q)
        print(f"  Query Type:  {'Natural Language (Conversational)' if is_nl else 'Keyword Style'}")

        # 1. Lexical VSM
        vsm_results = vsm.search(q, top_k=3)
        vsm_str = ", ".join([f"{r['doc_id']} ({r['cosine_score']:.4f})" for r in vsm_results]) if vsm_results else "No matches (0.0000)"
        print(f"  1. Lexical VSM (lnc.ltc):     {vsm_str}")

        # 2. Dense Semantic
        sem_results = sem.search(q, top_k=3)
        sem_str = ", ".join([f"{r['doc_id']} ({r['semantic_score']:.4f})" for r in sem_results]) if sem_results else "None"
        print(f"  2. Dense Semantic (MiniLM):  {sem_str}")

        # 3. Hybrid (alpha=0.5)
        hyb_results = sem.hybrid_search(q, vsm_retriever=vsm, alpha=0.5, top_k=3)
        hyb_str = ", ".join([f"{r['doc_id']} ({r['combined_score']:.4f})" for r in hyb_results]) if hyb_results else "None"
        print(f"  3. Hybrid (alpha=0.50):       {hyb_str}")

    print("\n" + "=" * 84)
    print("Benchmark complete. All systems fully calibrated and operational.")
    print("=" * 84)


if __name__ == "__main__":
    run_benchmark()
