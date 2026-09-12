"""
Services Package for Clothing IR Engine
=======================================
Provides singleton access to IR indexing and retrieval engines.
"""

from typing import Dict, Any, Optional
from pathlib import Path
from .preprocessor import Preprocessor, PorterStemmer
from .indexer import ClothingCorpusIndex
from .vsm_service import VSMRetriever
from .positional_service import PositionalSearcher
from .advanced_ir import AdvancedIREngine
from .semantic_service import SemanticSearchService
from .spelling_service import SpellingService
from .synonym_service import ClothingThesaurusService

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
        spelling = SpellingService(index)
        synonyms = ClothingThesaurusService(index)

        output_dir = Path(corpus_path).resolve().parent.parent / "output"
        semantic_pkl = output_dir / "semantic_index.pkl"
        semantic = SemanticSearchService(
            index_path=str(semantic_pkl) if semantic_pkl.exists() else None
        )
        if not semantic.is_loaded:
            try:
                semantic.build_index(index.documents, save_path=str(semantic_pkl))
            except Exception as e:
                print(f"Notice: Semantic index build deferred: {e}")

        _ir_instances[corpus_path] = {
            "index": index,
            "vsm": vsm,
            "positional": positional,
            "advanced": advanced,
            "semantic": semantic,
            "spelling": spelling,
            "synonyms": synonyms
        }
    return _ir_instances[corpus_path]


__all__ = [
    "Preprocessor",
    "PorterStemmer",
    "ClothingCorpusIndex",
    "VSMRetriever",
    "PositionalSearcher",
    "AdvancedIREngine",
    "SemanticSearchService",
    "SpellingService",
    "ClothingThesaurusService",
    "get_ir_system"
]
