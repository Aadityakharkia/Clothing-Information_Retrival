"""
Semantic Index Builder CLI Script
=================================
Pre-computes dense 384-dimensional embeddings for all 100 garments
using `all-MiniLM-L6-v2` and serializes the matrix to `output/semantic_index.pkl`.
"""

import os
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.config import get_config
from backend.app.services.indexer import ClothingCorpusIndex
from backend.app.services.semantic_service import SemanticSearchService


def build_semantic():
    cfg = get_config()
    print("============================================================")
    print("Building Offline Semantic Index (all-MiniLM-L6-v2)")
    print(f"Corpus Path: {cfg.CORPUS_PATH}")
    save_path = os.path.join(cfg.OUTPUT_PATH, SemanticSearchService.DEFAULT_INDEX_FILENAME)
    print(f"Target Path: {save_path}")
    print("============================================================")

    t0 = time.time()
    corpus_index = ClothingCorpusIndex(cfg.CORPUS_PATH)
    print(f"✓ Parsed {corpus_index.total_docs} documents from corpus.")

    print("Encoding documents into dense 384-dim semantic space on local CPU...")
    service = SemanticSearchService()
    embeddings = service.build_index(corpus_index.documents, save_path=save_path)
    elapsed = round(time.time() - t0, 2)

    print(f"✓ Successfully generated embeddings matrix: shape {embeddings.shape}")
    print(f"✓ Saved serialized semantic index to: {save_path}")
    print(f"✓ Total build time: {elapsed}s")
    print("Semantic index build complete!")


if __name__ == "__main__":
    build_semantic()
