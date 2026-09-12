"""
Autocomplete Controller
=======================
Handles prefix autocompletions, scoped department suggestions, and product previews.
"""

import time
from typing import Dict, Any
from flask import g, has_app_context
from ..services import get_ir_system


def handle_autocomplete(
    query: str = "",
    limit: int = 8,
    corpus_path: str = None
) -> Dict[str, Any]:
    """
    Orchestrates suggestions for the search autocomplete bar.
    """
    t0 = time.time()
    ir = get_ir_system(corpus_path)
    autocomplete = ir["autocomplete"]

    data = autocomplete.suggest(query=query, limit=limit)

    duration_ms = round((time.time() - t0) * 1000, 2)
    token = getattr(getattr(g, "request_trace", None), "token", None) if has_app_context() else None

    return {
        "success": True,
        "query": data["query"],
        "is_empty": data["is_empty"],
        "suggestions": data["suggestions"],
        "categories": data["categories"],
        "products": data["products"],
        "corrected_from": data["corrected_from"],
        "execution_time_ms": duration_ms,
        "request_token": token
    }
