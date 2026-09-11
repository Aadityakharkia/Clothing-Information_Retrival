"""
Semantic Search Controller
==========================
Orchestrates dense semantic retrieval and hybrid scoring requests.
"""

import time
from typing import Dict, Any
from flask import g
from ..services import get_ir_system


def handle_semantic_search(
    query: str,
    mode: str = "hybrid",
    alpha: float = 0.5,
    top_k: int = 10,
    corpus_path: str = None
) -> Dict[str, Any]:
    """
    Handles semantic search requests:
    - mode="semantic": Pure dense cosine similarity
    - mode="hybrid": Blended alpha * semantic + (1 - alpha) * VSM lnc.ltc
    - mode="auto": If natural language, uses hybrid/semantic; otherwise uses VSM
    """
    t0 = time.time()
    ir = get_ir_system(corpus_path)
    semantic_service = ir["semantic"]
    vsm = ir["vsm"]

    is_nl = semantic_service.is_natural_language(query)

    effective_mode = mode
    if mode == "auto":
        effective_mode = "hybrid" if is_nl else "vsm"

    if effective_mode == "semantic":
        results = semantic_service.search(query, top_k=top_k)
    elif effective_mode == "hybrid":
        results = semantic_service.hybrid_search(
            query,
            vsm_retriever=vsm,
            alpha=alpha,
            top_k=top_k
        )
    else:  # fallback to pure VSM
        results = vsm.search(query, top_k=top_k)
        for r in results:
            r["combined_score"] = r["cosine_score"]

    duration_ms = round((time.time() - t0) * 1000, 2)
    from flask import has_app_context
    token = getattr(getattr(g, "request_trace", None), "token", None) if has_app_context() else None

    return {
        "success": True,
        "query": query,
        "mode": effective_mode,
        "requested_mode": mode,
        "is_natural_language": is_nl,
        "alpha": alpha if effective_mode == "hybrid" else None,
        "total_results": len(results),
        "results": results,
        "execution_time_ms": duration_ms,
        "request_token": token
    }
