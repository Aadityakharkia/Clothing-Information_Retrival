"""
Unit Test Suite for Information Retrieval Engine (CSD358)
=========================================================
Tests all core components:
1. Preprocessor: Tokenization, Case Normalization, Stop-word removal, Porter Stemming
2. Indexer: Inverted and Positional Indices consistency
3. VSM: lnc.ltc weighting, cosine normalization, score correctness, tie-breaking
4. Positional Search: Exact Phrase, Ordered Proximity (WITHIN/k)
5. Out-of-Vocabulary handling
6. Advanced IR: Positional Hybrid Boost, Positional Intersect Tracer, Rocchio Feedback
"""

import math
import pytest
from src.preprocessor import Preprocessor, PorterStemmer
from src.indexer import ClothingCorpusIndex
from src.vsm import VSMRetriever
from src.positional_search import PositionalSearcher
from src.advanced_ir import AdvancedIREngine

CORPUS_PATH = "data/corpus.txt"


@pytest.fixture(scope="module")
def ir_system():
    index = ClothingCorpusIndex(CORPUS_PATH)
    vsm = VSMRetriever(index)
    positional = PositionalSearcher(index)
    advanced = AdvancedIREngine(index, vsm)
    return {
        "index": index,
        "vsm": vsm,
        "positional": positional,
        "advanced": advanced
    }


def test_stemmer():
    stemmer = PorterStemmer()
    assert stemmer.stem("running") == "run"
    assert stemmer.stem("shirts") == "shirt"
    assert stemmer.stem("cotton") == "cotton"
    assert stemmer.stem("washable") == "washabl"
    assert stemmer.stem("printed") == "print"


def test_preprocessing():
    prep = Preprocessor()
    tokens = prep.preprocess("Men's Cotton Crew Neck T-Shirt - Black!")
    assert "cotton" in tokens
    assert "shirt" in tokens
    assert "black" in tokens
    # Stop words like 'is', 'the', 'and' must be filtered
    assert "is" not in prep.preprocess("This is the best cotton shirt")


def test_index_structure(ir_system):
    index = ir_system["index"]
    assert index.total_docs == 100
    assert len(index.vocabulary) > 100
    assert "cotton" in index.inverted_index
    assert "shirt" in index.positional_index

    # Check positional index structure
    shirt_pos_entry = index.positional_index["shirt"]
    assert "df" in shirt_pos_entry
    assert "postings" in shirt_pos_entry
    first_posting = shirt_pos_entry["postings"][0]
    assert len(first_posting) == 3  # (docID, tf, positions)
    assert isinstance(first_posting[2], list)


def test_vsm_lnc_ltc_scoring(ir_system):
    vsm = ir_system["vsm"]
    results = vsm.search("cotton crew neck t-shirt", top_k=10)
    assert len(results) <= 10
    assert len(results) > 0

    # Scores must be sorted in descending order
    scores = [r["cosine_score"] for r in results]
    assert scores == sorted(scores, reverse=True)

    # Scores must be between 0.0 and 1.0
    for s in scores:
        assert 0.0 <= s <= 1.0

    # Ties must be broken by increasing docID
    for i in range(len(results) - 1):
        if results[i]["cosine_score"] == results[i+1]["cosine_score"]:
            assert results[i]["doc_id"] < results[i+1]["doc_id"]


def test_out_of_vocabulary_query(ir_system):
    vsm = ir_system["vsm"]
    results = vsm.search("cyberpunk xenomorph rainwear")
    assert results == []


def test_exact_phrase_search(ir_system):
    pos_searcher = ir_system["positional"]
    results = pos_searcher.search_exact_phrase('"cotton shirt"')
    assert len(results) > 0
    for r in results:
        assert "matched_positions" in r
        for match in r["matched_positions"]:
            # Consecutive tokens: pos[1] == pos[0] + 1
            assert match[1] == match[0] + 1


def test_proximity_search_within_k(ir_system):
    pos_searcher = ir_system["positional"]
    results = pos_searcher.search_proximity("winter", "wear", k=3)
    assert len(results) > 0
    for r in results:
        assert "matched_pairs" in r
        for p1, p2, dist in r["matched_pairs"]:
            assert 0 < p2 - p1 <= 3
            assert dist == p2 - p1


def test_positional_hybrid_boost(ir_system):
    advanced = ir_system["advanced"]
    results = advanced.search_hybrid_proximity_boost("stretch denim", lambda_param=0.5, top_k=5)
    assert len(results) > 0
    for r in results:
        assert "hybrid_score" in r
        assert "boost_factor" in r
        assert r["hybrid_score"] >= r["vsm_score"]


def test_positional_intersection_tracer(ir_system):
    advanced = ir_system["advanced"]
    trace = advanced.trace_positional_intersect("stretch", "denim", k=4)
    assert "matches" in trace
    assert "trace_log" in trace
    assert len(trace["trace_log"]) > 0


def test_rocchio_relevance_feedback(ir_system):
    advanced = ir_system["advanced"]
    # Mark D001 as relevant for "t-shirt"
    feedback = advanced.rocchio_feedback(
        query="t-shirt",
        relevant_doc_ids=["D001"],
        irrelevant_doc_ids=[],
        top_k=5
    )
    assert "top_expanded_terms" in feedback
    assert "results" in feedback
    assert len(feedback["results"]) > 0
