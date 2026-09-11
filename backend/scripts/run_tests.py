"""
Part E Test Suite Runner CLI Script
===================================
Executes mandatory Part E evaluation queries and writes test report artifacts.
"""

import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.test_runner import TestRunner
from backend.config import get_config

def main():
    cfg = get_config()
    print("Running Part E Mandatory Test Suite...")
    runner = TestRunner(cfg.CORPUS_PATH, cfg.OUTPUT_PATH)
    results = runner.run_all_tests()
    print(f"✓ Executed {len(results.get('free_text_tests', []))} free-text queries.")
    print(f"✓ Executed {len(results.get('exact_phrase_tests', []))} exact phrase queries.")
    print(f"✓ Executed {len(results.get('proximity_tests', []))} proximity queries.")
    print(f"✓ Test reports written to {cfg.OUTPUT_PATH}")

if __name__ == "__main__":
    main()
