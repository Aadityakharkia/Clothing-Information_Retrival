"""
Corpus Index Builder CLI Script
===============================
Parses raw corpus data and generates inverted & positional indices in output/.
"""

import os
import sys
from pathlib import Path

# Ensure project root is in path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.services.indexer import ClothingCorpusIndex
from backend.config import get_config

def build():
    cfg = get_config()
    print("Building Inverted & Positional Indices...")
    print(f"Corpus: {cfg.CORPUS_PATH}")
    print(f"Output: {cfg.OUTPUT_PATH}")

    index = ClothingCorpusIndex(cfg.CORPUS_PATH)
    index.save_indices(cfg.OUTPUT_PATH)

    print(f"✓ Processed {index.total_docs} documents.")
    print(f"✓ Vocabulary size: {len(index.vocabulary)} terms.")
    print("Index build successful.")

if __name__ == "__main__":
    build()
