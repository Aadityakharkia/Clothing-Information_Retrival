"""
Document Data Model for Clothing IR Engine
==========================================
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any


@dataclass
class Document:
    """Represents a clothing product document in the corpus."""
    doc_id: str
    category: str
    title: str
    text: str
    combined_text: str = field(init=False)
    tokens: List[Tuple[str, int, int, int]] = field(default_factory=list)  # (term, pos, start_char, end_char)
    tf_dict: Dict[str, int] = field(default_factory=dict)
    positions_dict: Dict[str, List[int]] = field(default_factory=dict)
    char_spans_dict: Dict[str, List[Tuple[int, int]]] = field(default_factory=dict)
    vector_length: float = 0.0  # Euclidean length under lnc

    def __post_init__(self):
        self.combined_text = f"{self.title}. {self.text}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "category": self.category,
            "title": self.title,
            "text": self.text,
            "vector_length": round(self.vector_length, 4)
        }
