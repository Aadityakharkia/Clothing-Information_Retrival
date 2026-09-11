"""
Tracer Controller
=================
Orchestrates step-by-step positional intersection tracing.
"""

import time
from typing import Dict, Any
from flask import g
from ..services import get_ir_system


def handle_trace(term1: str, term2: str, k: int, corpus_path: str) -> Dict[str, Any]:
    t0 = time.time()
    ir = get_ir_system(corpus_path)
    advanced = ir["advanced"]

    result = advanced.trace_positional_intersect(term1, term2, k=k)
    duration_ms = round((time.time() - t0) * 1000, 2)
    token = getattr(getattr(g, "request_trace", None), "token", None)

    return {
        "success": True,
        **result,
        "execution_time_ms": duration_ms,
        "request_token": token
    }
