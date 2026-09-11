"""
Services Package for Clothing IR Engine
=======================================
Provides singleton access to IR indexing and retrieval engines.
"""

from typing import Dict, Any, Optional
from .preprocessor import Preprocessor, PorterStemmer
from .indexer import ClothingCorpusIndex
from .vsm_service import VSMRetriever
from .positional_service import PositionalSearcher
from .advanced_ir import AdvancedIREngine

_ir_instances: Dict[str, Any] = {}


def get_ir_system(corpus_path: str) -> Dict[str, Any]:
    """
    Returns cached singleton IR engine instances initialized from the given corpus.
    Thread-safe lazy initialization.
    """
    global _ir_instances
    if corpus_path not in _ir_instances:
        index = ClothingCorpusIndex(corpus_path)
        vsm = VSMRetriever(index)
        positional = PositionalSearcher(index)
        advanced = AdvancedIREngine(index, vsm)
        _ir_instances[corpus_path] = {
            "index": index,
            "vsm": vsm,
            "positional": positional,
            "advanced": advanced
        }
    return _ir_instances[corpus_path]


__all__ = [
    "Preprocessor",
    "PorterStemmer",
    "ClothingCorpusIndex",
    "VSMRetriever",
    "PositionalSearcher",
    "AdvancedIREngine",
    "get_ir_system"
]
