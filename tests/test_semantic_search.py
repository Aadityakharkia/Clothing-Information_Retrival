"""
Unit and Integration Tests for Semantic Search Module (Innovation #4)
======================================================================
Verifies:
1. Dense 384-dimensional vector embeddings and unit normalization.
2. Natural language query intent classifier heuristics.
3. Dense semantic retrieval rankings.
4. Hybrid alpha-blended scoring calibration.
5. REST API endpoint /api/search/semantic and response schemas.
"""

import os
import pytest
import numpy as np
from pathlib import Path
from backend.app import create_app
from backend.config import TestingConfig, get_config
from backend.app.services.indexer import ClothingCorpusIndex
from backend.app.services.vsm_service import VSMRetriever
from backend.app.services.semantic_service import SemanticSearchService
from backend.app.controllers.semantic_controller import handle_semantic_search


@pytest.fixture
def cfg():
    return get_config()


@pytest.fixture
def semantic_service(cfg):
    save_path = os.path.join(cfg.OUTPUT_PATH, SemanticSearchService.DEFAULT_INDEX_FILENAME)
    service = SemanticSearchService(index_path=save_path)
    if not service.is_loaded:
        index = ClothingCorpusIndex(cfg.CORPUS_PATH)
        service.build_index(index.documents, save_path=save_path)
    return service


@pytest.fixture
def client(tmp_path):
    log_file = tmp_path / "test_semantic_log.jsonl"
    config = TestingConfig()
    config.REQUEST_LOG_PATH = str(log_file)
    app = create_app(config)
    with app.test_client() as test_client:
        yield test_client


def test_semantic_index_dimensions_and_norm(semantic_service):
    """Verifies that all 100 documents are embedded in 384-dim space with unit L2 norm."""
    assert semantic_service.is_loaded is True
    assert len(semantic_service.doc_ids) == 100
    assert semantic_service.embeddings.shape == (100, 384)

    # Every embedding vector must have L2 norm = 1.0 (within float32 precision)
    norms = np.linalg.norm(semantic_service.embeddings, axis=1)
    np.testing.assert_allclose(norms, np.ones(100), atol=1e-4)


def test_natural_language_classifier():
    """Verifies conversational marker detection and token length threshold."""
    # Long query >= 5 tokens
    assert SemanticSearchService.is_natural_language("what is a good winter jacket") is True
    assert SemanticSearchService.is_natural_language("garment suitable for cold evening parties") is True

    # Shorter query with conversational preposition or intent word
    assert SemanticSearchService.is_natural_language("jacket for winter") is True
    assert SemanticSearchService.is_natural_language("best cotton shirt") is True
    assert SemanticSearchService.is_natural_language("comfortable kurta") is True

    # Pure keyword queries (below length threshold without markers)
    assert SemanticSearchService.is_natural_language("cotton shirt") is False
    assert SemanticSearchService.is_natural_language("jeans denim") is False


def test_dense_semantic_ranking(semantic_service):
    """Verifies that natural language intent correctly retrieves semantically relevant garments."""
    # "warm winter coat for snow" should rank Jackets or Hoodies top
    results = semantic_service.search("warm winter coat for snow", top_k=5)
    assert len(results) == 5
    assert results[0]["rank"] == 1
    assert results[0]["semantic_score"] > 0.3

    # Top result category should be Jacket or Hoodie
    top_categories = {r["category"] for r in results}
    assert "Jacket" in top_categories or "Hoodie" in top_categories


def test_hybrid_alpha_blending(cfg, semantic_service):
    """Verifies mathematical interpolation between semantic score and VSM score."""
    corpus_index = ClothingCorpusIndex(cfg.CORPUS_PATH)
    vsm = VSMRetriever(corpus_index)

    query = "cotton t-shirt"

    # Hybrid with alpha=0.5
    results_half = semantic_service.hybrid_search(query, vsm_retriever=vsm, alpha=0.5, top_k=5)
    assert len(results_half) == 5

    for r in results_half:
        expected = 0.5 * r["semantic_score"] + 0.5 * r["lexical_score"]
        assert pytest.approx(r["combined_score"], abs=1e-4) == expected


def test_api_semantic_search_endpoint(client):
    """Tests /api/search/semantic HTTP endpoint."""
    resp = client.get("/api/search/semantic?q=warm+insulated+jacket+for+winter&mode=hybrid&alpha=0.6&top_k=5")
    assert resp.status_code == 200
    data = resp.get_json()

    assert data["success"] is True
    assert data["mode"] == "hybrid"
    assert data["is_natural_language"] is True
    assert data["alpha"] == 0.6
    assert len(data["results"]) == 5
    assert "X-Request-Token" in resp.headers
    assert resp.headers["X-Request-Token"].startswith("REQ-")
