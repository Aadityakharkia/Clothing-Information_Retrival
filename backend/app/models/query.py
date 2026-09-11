"""
Query Request and Response Data Contracts
=========================================
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class SearchRequest:
    """Standardized search query parameters."""
    query: str
    mode: str = "vsm"  # 'vsm', 'positional', 'hybrid'
    top_k: int = 10
    proximity_k: int = 3
    lambda_param: float = 0.5


@dataclass
class SearchResultItem:
    """Individual ranked search hit."""
    rank: int
    doc_id: str
    category: str
    title: str
    text: str
    score: float
    score_type: str = "cosine_score"
    term_contributions: Dict[str, float] = field(default_factory=dict)
    matched_positions: List[Any] = field(default_factory=list)
    vector_length: float = 0.0


@dataclass
class SearchResponse:
    """Structured response payload for all search endpoints."""
    success: bool
    query: str
    mode: str
    total_results: int
    results: List[Dict[str, Any]]
    execution_time_ms: float
    request_token: Optional[str] = None
    query_details: Optional[Dict[str, Any]] = None
