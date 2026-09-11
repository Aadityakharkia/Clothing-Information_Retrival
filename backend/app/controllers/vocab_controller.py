"""
Vocabulary & Index Explorer Controller
======================================
"""

import math
import time
from typing import Dict, Any, List
from flask import g
from ..services import get_ir_system


def handle_get_vocabulary(corpus_path: str, search: str = "", page: int = 1, per_page: int = 2000) -> Dict[str, Any]:
    t0 = time.time()
    ir = get_ir_system(corpus_path)
    index = ir["index"]

    terms = index.vocabulary
    if search:
        search_lower = search.strip().lower()
        terms = [t for t in terms if search_lower in t]

    total_terms = len(terms)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_terms = terms[start_idx:end_idx]

    items = []
    for term in page_terms:
        inv_entry = index.inverted_index.get(term, {"df": 0, "postings": []})
        pos_entry = index.positional_index.get(term, {"df": 0, "postings": []})

        df = inv_entry.get("df", 0)
        idf = round(math.log10(index.total_docs / df), 4) if df > 0 else 0.0

        inv_postings = inv_entry.get("postings", [])
        postings_preview = []
        if isinstance(inv_postings, list):
            for p in inv_postings[:6]:
                if isinstance(p, (list, tuple)) and len(p) >= 2:
                    postings_preview.append({"doc_id": p[0], "tf": p[1]})
                elif isinstance(p, dict):
                    postings_preview.append(p)

        pos_postings = pos_entry.get("postings", [])
        sample_positions = []
        if isinstance(pos_postings, list) and len(pos_postings) > 0:
            first_pos = pos_postings[0]
            if isinstance(first_pos, (list, tuple)) and len(first_pos) >= 3:
                sample_positions = first_pos[2][:5]

        items.append({
            "term": term,
            "df": df,
            "idf": idf,
            "postings": postings_preview,
            "postings_preview": postings_preview,
            "sample_positions": sample_positions,
            "has_more_postings": len(inv_postings) > 6
        })

    duration_ms = round((time.time() - t0) * 1000, 2)
    token = getattr(getattr(g, "request_trace", None), "token", None)

    return {
        "success": True,
        "total_terms": total_terms,
        "page": page,
        "per_page": per_page,
        "total_pages": math.ceil(total_terms / per_page) if per_page > 0 else 1,
        "items": items,
        "terms": items,  # Alias for template backward-compatibility
        "execution_time_ms": duration_ms,
        "request_token": token
    }
