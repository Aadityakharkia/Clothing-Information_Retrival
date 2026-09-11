"""
Test Suite Controller (CSD358 Part E)
=====================================
Orchestrates Part E mandatory test queries and comparative analyses.
"""

import time
from typing import Dict, Any
from flask import g
from ..services import get_ir_system

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
    "waterproof cyberpunk rainwear"  # OOV query
]

EXACT_PHRASE_QUERIES = [
    '"cotton shirt"',
    '"stretch denim"',
    '"festive wear"',
    '"winter wear"',
    '"regular fit"'
]

PROXIMITY_QUERIES = [
    ("cotton WITHIN/3 shirt", "cotton", "shirt", 3),
    ("stretch WITHIN/4 denim", "stretch", "denim", 4),
    ("winter WITHIN/3 wear", "winter", "wear", 3),
    ("festive WITHIN/4 kurta", "festive", "kurta", 4)
]


def handle_run_tests(corpus_path: str) -> Dict[str, Any]:
    t0 = time.time()
    ir = get_ir_system(corpus_path)
    vsm = ir["vsm"]
    pos = ir["positional"]
    adv = ir["advanced"]

    ft_results = []
    for q in FREE_TEXT_QUERIES:
        res = vsm.search(q, top_k=5)
        ft_results.append({
            "query": q,
            "is_oov": len(res) == 0,
            "total_matches": len(res),
            "top_docs": [(r["doc_id"], r["cosine_score"]) for r in res[:3]]
        })

    phrase_results = []
    for p in EXACT_PHRASE_QUERIES:
        res = pos.search_exact_phrase(p)
        phrase_results.append({
            "query": p,
            "total_matches": len(res),
            "matched_doc_ids": [r["doc_id"] for r in res[:5]],
            "sample_positions": res[0]["matched_positions"][:3] if res else []
        })

    prox_results = []
    for raw_q, t1, t2, k in PROXIMITY_QUERIES:
        res = pos.search_proximity(t1, t2, k)
        prox_results.append({
            "query": raw_q,
            "term1": t1,
            "term2": t2,
            "k": k,
            "total_matches": len(res),
            "matched_doc_ids": [r["doc_id"] for r in res[:5]],
            "sample_pairs": res[0]["matched_pairs"][:3] if res else []
        })

    # Comparative analysis case studies
    comp1_vsm = vsm.search("cotton shirt", top_k=5)
    comp1_pos = pos.search_exact_phrase('"cotton shirt"')
    comp1_hybrid = adv.search_hybrid_proximity_boost("cotton shirt", top_k=5)

    comp2_vsm = vsm.search("stretch denim", top_k=5)
    comp2_prox = pos.search_proximity("stretch", "denim", k=4)
    comp2_hybrid = adv.search_hybrid_proximity_boost("stretch denim", top_k=5)

    comparative = [
        {
            "case": "Case 1: 'cotton shirt' (Bag-of-Words vs Exact Consecutive Phrase)",
            "vsm_top3": [r["doc_id"] for r in comp1_vsm[:3]],
            "positional_docs": [r["doc_id"] for r in comp1_pos[:3]],
            "hybrid_top3": [r["doc_id"] for r in comp1_hybrid[:3]],
            "analysis": "Bag-of-words VSM matches documents containing 'cotton' and 'shirt' anywhere in the description, whereas positional search strictly enforces that 'shirt' immediately follows 'cotton' (p2 = p1 + 1), filtering out documents where words appear in separate paragraphs."
        },
        {
            "case": "Case 2: 'stretch denim' (Proximity WITHIN/4 vs Pure Cosine)",
            "vsm_top3": [r["doc_id"] for r in comp2_vsm[:3]],
            "positional_docs": [r["doc_id"] for r in comp2_prox[:3]],
            "hybrid_top3": [r["doc_id"] for r in comp2_hybrid[:3]],
            "analysis": "Proximity verification requires 'denim' within 4 words after 'stretch'. In hybrid boosting, documents with tighter spans receive a substantial proximity bonus, reordering documents where fabric stretch properties describe the denim directly."
        }
    ]

    duration_ms = round((time.time() - t0) * 1000, 2)
    token = getattr(getattr(g, "request_trace", None), "token", None)

    return {
        "success": True,
        "free_text_tests": ft_results,
        "exact_phrase_tests": phrase_results,
        "proximity_tests": prox_results,
        "comparative_analysis": comparative,
        "execution_time_ms": duration_ms,
        "request_token": token
    }
