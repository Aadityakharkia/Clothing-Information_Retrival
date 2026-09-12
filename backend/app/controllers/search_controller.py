"""
Search Controller
=================
Handles orchestration for free-text VSM, positional phrase, and hybrid proximity searches.
"""

import time
from typing import Dict, Any
from flask import g, has_app_context
from ..services import get_ir_system


def handle_vsm_search(
    query: str,
    top_k: int = 100,
    autocorrect: bool = True,
    synonyms: bool = True,
    corpus_path: str = None
) -> Dict[str, Any]:
    t0 = time.time()
    ir = get_ir_system(corpus_path)
    vsm = ir["vsm"]
    spelling = ir["spelling"]
    thesaurus = ir["synonyms"]

    # 1. Spelling Correction
    spell_info = spelling.correct_query(query)
    was_corrected = spell_info["was_corrected"] if autocorrect else False
    effective_query = spell_info["corrected_query"] if was_corrected else query

    # 2. Synonym & Apparel Expansion
    expansion_info = thesaurus.expand_query(effective_query) if synonyms else {
        "expanded_query_str": effective_query,
        "term_weights": {},
        "synonym_map": {},
        "has_expansions": False,
        "expanded_terms": []
    }

    # 3. Perform VSM Retrieval
    # If synonyms are enabled and expansions exist, pass term_weights to softly boost primary vs synonyms
    if synonyms and expansion_info["has_expansions"]:
        search_query = expansion_info["expanded_query_str"]
        results = vsm.search(
            search_query,
            top_k=top_k,
            term_weights_override=expansion_info["term_weights"]
        )
        _, _, query_details = vsm.compute_query_weights(
            search_query,
            term_weights_override=expansion_info["term_weights"]
        )
    else:
        results = vsm.search(effective_query, top_k=top_k)
        _, _, query_details = vsm.compute_query_weights(effective_query)

    duration_ms = round((time.time() - t0) * 1000, 2)
    token = getattr(getattr(g, "request_trace", None), "token", None) if has_app_context() else None

    return {
        "success": True,
        "query": query,
        "effective_query": effective_query,
        "was_corrected": was_corrected,
        "suggested_query": spell_info["corrected_query"] if spell_info["was_corrected"] else None,
        "corrections": spell_info["corrections"] if was_corrected else {},
        "has_synonyms": expansion_info["has_expansions"],
        "expanded_terms": expansion_info["expanded_terms"],
        "synonym_map": expansion_info["synonym_map"],
        "mode": "vsm",
        "total_results": len(results),
        "results": results,
        "query_details": query_details,
        "execution_time_ms": duration_ms,
        "request_token": token
    }


def handle_positional_search(query: str, corpus_path: str = None) -> Dict[str, Any]:
    t0 = time.time()
    ir = get_ir_system(corpus_path)
    pos_searcher = ir["positional"]

    query_type, results = pos_searcher.parse_and_search(query)

    duration_ms = round((time.time() - t0) * 1000, 2)
    token = getattr(getattr(g, "request_trace", None), "token", None) if has_app_context() else None

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


def handle_hybrid_search(query: str, lambda_param: float = 0.5, top_k: int = 100, corpus_path: str = None) -> Dict[str, Any]:
    t0 = time.time()
    ir = get_ir_system(corpus_path)
    advanced = ir["advanced"]

    results = advanced.search_hybrid_proximity_boost(query, lambda_param=lambda_param, top_k=top_k)

    duration_ms = round((time.time() - t0) * 1000, 2)
    token = getattr(getattr(g, "request_trace", None), "token", None) if has_app_context() else None

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
