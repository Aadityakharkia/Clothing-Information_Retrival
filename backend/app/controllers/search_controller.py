"""
Search Controller
=================
Handles orchestration for free-text VSM, positional phrase, and hybrid proximity searches.
"""

import time
from typing import Dict, Any
from flask import g
from ..services import get_ir_system


def handle_vsm_search(query: str, top_k: int, corpus_path: str) -> Dict[str, Any]:
    t0 = time.time()
    ir = get_ir_system(corpus_path)
    vsm = ir["vsm"]

    results = vsm.search(query, top_k=top_k)
    _, _, query_details = vsm.compute_query_weights(query)

    duration_ms = round((time.time() - t0) * 1000, 2)
    token = getattr(getattr(g, "request_trace", None), "token", None)

    return {
        "success": True,
        "query": query,
        "mode": "vsm",
        "total_results": len(results),
        "results": results,
        "query_details": query_details,
        "execution_time_ms": duration_ms,
        "request_token": token
    }


def handle_positional_search(query: str, corpus_path: str) -> Dict[str, Any]:
    t0 = time.time()
    ir = get_ir_system(corpus_path)
    pos_searcher = ir["positional"]

    query_type, results = pos_searcher.parse_and_search(query)

    duration_ms = round((time.time() - t0) * 1000, 2)
    token = getattr(getattr(g, "request_trace", None), "token", None)

    return {
        "success": True,
        "query": query,
        "mode": "positional",
        "query_type": query_type,
        "total_results": len(results),
        "results": results,
        "execution_time_ms": duration_ms,
        "request_token": token
    }


def handle_hybrid_search(query: str, lambda_param: float, top_k: int, corpus_path: str) -> Dict[str, Any]:
    t0 = time.time()
    ir = get_ir_system(corpus_path)
    advanced = ir["advanced"]

    results = advanced.search_hybrid_proximity_boost(query, lambda_param=lambda_param, top_k=top_k)

    duration_ms = round((time.time() - t0) * 1000, 2)
    token = getattr(getattr(g, "request_trace", None), "token", None)

    return {
        "success": True,
        "query": query,
        "mode": "hybrid",
        "lambda": lambda_param,
        "total_results": len(results),
        "results": results,
        "execution_time_ms": duration_ms,
        "request_token": token
    }
