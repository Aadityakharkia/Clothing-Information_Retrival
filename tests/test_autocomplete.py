"""
Tests for Autocomplete & Autofill Suggestion Service
=====================================================
Validates prefix query completions, category-scoped suggestions,
direct product matches, typo tolerance, and the /api/suggest endpoint.
"""

import pytest
from backend.app import create_app
from backend.app.services.indexer import ClothingCorpusIndex
from backend.app.services.spelling_service import SpellingService
from backend.app.services.autocomplete_service import AutocompleteService


@pytest.fixture(scope="module")
def corpus_index():
    return ClothingCorpusIndex("data/corpus.txt")


@pytest.fixture(scope="module")
def spelling(corpus_index):
    return SpellingService(corpus_index)


@pytest.fixture(scope="module")
def autocomplete(corpus_index, spelling):
    return AutocompleteService(corpus_index, spelling)


@pytest.fixture(scope="module")
def test_client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_autocomplete_prefix_match(autocomplete):
    res = autocomplete.suggest("cot", limit=8)
    assert res["query"] == "cot"
    assert not res["is_empty"]
    assert len(res["suggestions"]) > 0

    # Ensure suggestions start with prefix or contain relevant cotton phrases
    texts = [s["text"].lower() for s in res["suggestions"]]
    assert any("cotton" in t for t in texts)

    # Check prefix and completion formatting
    first_query = next((s for s in res["suggestions"] if s["type"] == "query"), None)
    assert first_query is not None
    assert first_query["display_prefix"].lower() == "cot"
    assert len(first_query["display_completion"]) > 0


def test_autocomplete_category_scope(autocomplete):
    res = autocomplete.suggest("cotton", limit=8)
    scopes = [s for s in res["suggestions"] if s["type"] == "category_scope"]
    assert len(scopes) > 0
    first_scope = scopes[0]
    assert "category" in first_scope
    assert " in " in first_scope["displayText"]
    assert first_scope["category"] in ["T-Shirt", "Shirt", "Kurta", "Saree", "Dress"]


def test_autocomplete_product_matches(autocomplete):
    res = autocomplete.suggest("denim jeans", limit=5)
    assert len(res["products"]) > 0
    first_prod = res["products"][0]
    assert "doc_id" in first_prod
    assert "title" in first_prod
    assert "category" in first_prod
    assert first_prod["doc_id"].startswith("D")


def test_autocomplete_typo_correction(autocomplete):
    # 'cotn' is a typo for 'cotton'
    res = autocomplete.suggest("cotn", limit=6)
    assert res["corrected_from"] == "cotn"
    texts = [s["text"].lower() for s in res["suggestions"]]
    assert any("cotton" in t for t in texts)


def test_autocomplete_empty_query(autocomplete):
    res = autocomplete.suggest("", limit=8)
    assert res["is_empty"] is True
    assert len(res["suggestions"]) > 0
    assert all(s["type"] == "popular" for s in res["suggestions"])
    assert len(res["categories"]) > 0


def test_api_suggest_endpoint(test_client):
    response = test_client.get("/api/suggest?q=hoodie&limit=5")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["query"] == "hoodie"
    assert "suggestions" in data
    assert "products" in data
    assert "execution_time_ms" in data
    assert len(data["suggestions"]) <= 5
