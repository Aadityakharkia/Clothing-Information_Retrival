"""
Assignment Deliverables Exporter & Packager (CSD358)
====================================================
Automates the end-to-end deliverable generation:
1. Generates Inverted Index & Positional Index outputs (JSON & TXT)
2. Runs the mandatory test suite and writes the Markdown & JSON test reports
3. Creates the final submission ZIP file containing all required files:
   - Source code with comments/documentation (src/, web/, tests/)
   - Dictionary / Inverted index output (output/inverted_index.txt, inverted_index.json)
   - Positional index output (output/positional_index.txt, positional_index.json)
   - Test results & comparative analysis (output/test_results_report.md)
   - Screenshots of the web application and query results (screenshots/)
   - Complete README.md documentation
"""

import os
import sys
import zipfile
import shutil
from datetime import datetime

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.test_runner import TestRunner


def export():
    print("=" * 70)
    print("CSD358 Assignment 1 - Deliverables Generation & Packaging")
    print("=" * 70)

    corpus_path = os.path.join(BASE_DIR, "data", "corpus.txt")
    output_dir = os.path.join(BASE_DIR, "output")
    screenshots_dir = os.path.join(BASE_DIR, "screenshots")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(screenshots_dir, exist_ok=True)

    print("\n[1/3] Running Test Suite and Generating Index Outputs...")
    runner = TestRunner(corpus_path, output_dir)
    results = runner.run_all_tests()
    print(f"  ✓ Processed {runner.index.total_docs} documents.")
    print(f"  ✓ Built vocabulary of {len(runner.index.vocabulary)} terms.")
    print(f"  ✓ Saved inverted_index.json & inverted_index.txt")
    print(f"  ✓ Saved positional_index.json & positional_index.txt")
    print(f"  ✓ Executed 10 free-text, 5 phrase, 4 proximity queries.")
    print(f"  ✓ Generated output/test_results_report.md & test_results_report.json")

    print("\n[2/3] Checking Required Files for Submission Package...")
    files_to_bundle = [
        ("README.md", "README.md"),
        ("pytest.ini", "pytest.ini"),
        ("data/corpus.txt", "data/corpus.txt"),
        ("output/inverted_index.txt", "output/inverted_index.txt"),
        ("output/inverted_index.json", "output/inverted_index.json"),
        ("output/positional_index.txt", "output/positional_index.txt"),
        ("output/positional_index.json", "output/positional_index.json"),
        ("output/test_results_report.md", "output/test_results_report.md"),
        ("ARCHITECTURE.md", "ARCHITECTURE.md"),
        ("output/request_log.jsonl", "output/request_log.jsonl"),
    ]

    # Add all files in backend/
    backend_dir = os.path.join(BASE_DIR, "backend")
    if os.path.exists(backend_dir):
        for root, _, files in os.walk(backend_dir):
            for f in files:
                if not f.endswith(".pyc") and "__pycache__" not in root:
                    rel_path = os.path.relpath(os.path.join(root, f), BASE_DIR)
                    files_to_bundle.append((rel_path, rel_path))

    # Add all files in frontend/
    frontend_dir = os.path.join(BASE_DIR, "frontend")
    if os.path.exists(frontend_dir):
        for root, _, files in os.walk(frontend_dir):
            for f in files:
                if not f.endswith(".pyc") and "__pycache__" not in root:
                    rel_path = os.path.relpath(os.path.join(root, f), BASE_DIR)
                    files_to_bundle.append((rel_path, rel_path))

    # Add all files in src/
    src_dir = os.path.join(BASE_DIR, "src")
    if os.path.exists(src_dir):
        for f in os.listdir(src_dir):
            if f.endswith(".py"):
                files_to_bundle.append((os.path.join("src", f), os.path.join("src", f)))

    # Add all files in tests/
    tests_dir = os.path.join(BASE_DIR, "tests")
    if os.path.exists(tests_dir):
        for f in os.listdir(tests_dir):
            if f.endswith(".py"):
                files_to_bundle.append((os.path.join("tests", f), os.path.join("tests", f)))

    # Add web files
    web_dir = os.path.join(BASE_DIR, "web")
    if os.path.exists(web_dir):
        for root, _, files in os.walk(web_dir):
            for f in files:
                if not f.endswith(".pyc") and "__pycache__" not in root:
                    rel_path = os.path.relpath(os.path.join(root, f), BASE_DIR)
                    files_to_bundle.append((rel_path, rel_path))

    # Add screenshots
    if os.path.exists(screenshots_dir):
        for f in os.listdir(screenshots_dir):
            rel_path = os.path.relpath(os.path.join(screenshots_dir, f), BASE_DIR)
            files_to_bundle.append((rel_path, rel_path))

    print(f"  ✓ Total files identified for bundling: {len(files_to_bundle)}")

    zip_filename = "CSD358_Assignment1_Clothing_Search_Engine.zip"
    zip_path = os.path.join(BASE_DIR, zip_filename)

    print(f"\n[3/3] Creating Final ZIP Deliverable: {zip_filename}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_rel, zip_internal_path in files_to_bundle:
            abs_path = os.path.join(BASE_DIR, file_rel)
            if os.path.exists(abs_path):
                zipf.write(abs_path, os.path.join("Clothing-Information_Retrival", zip_internal_path))
                print(f"  + Added: {zip_internal_path}")

    zip_size_kb = os.path.getsize(zip_path) / 1024
    print(f"\n{'='*70}")
    print(f"SUCCESS! Deliverables packaged in: {zip_path} ({zip_size_kb:.1f} KB)")
    print(f"{'='*70}")


if __name__ == "__main__":
    export()
