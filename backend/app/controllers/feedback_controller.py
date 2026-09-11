"""
Relevance Feedback Controller (Rocchio Engine)
==============================================
"""

import time
from typing import Dict, Any, List
from flask import g
from ..services import get_ir_system


def handle_rocchio_feedback(
    query: str,
    relevant_ids: List[str],
    irrelevant_ids: List[str],
    top_k: int,
    corpus_path: str
) -> Dict[str, Any]:
    t0 = time.time()
    ir = get_ir_system(corpus_path)
    advanced = ir["advanced"]

    result = advanced.rocchio_feedback(
        query=query,
        relevant_doc_ids=relevant_ids,
        irrelevant_doc_ids=irrelevant_ids,
        top_k=top_k
    )

    duration_ms = round((time.time() - t0) * 1000, 2)
    token = getattr(getattr(g, "request_trace", None), "token", None)

    return {
        "success": True,
        **result,
        "execution_time_ms": duration_ms,
        "request_token": token
    }
