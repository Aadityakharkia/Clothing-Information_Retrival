"""
Test Suite: Typo-Tolerance Spelling Correction & Apparel Synonym Expansion
==========================================================================
Verifies that:
1. Typos ('coton shit') auto-correct to 'cotton shirt' and retrieve relevant products.
2. Misspellings ('hoddie') auto-correct to 'hoodie' and expand to retrieve sweaters/sweatshirts.
3. Garment terms without exact corpus matches ('sweater') expand to retrieve related winter wear.
4. Core lnc.ltc VSM mathematics remain intact.
"""

import pytest
from pathlib import Path
from backend.app.services.indexer import ClothingCorpusIndex
from backend.app.services.vsm_service import VSMRetriever
from backend.app.services.spelling_service import SpellingService
from backend.app.services.synonym_service import ClothingThesaurusService
from backend.app.controllers.search_controller import handle_vsm_search


CORPUS_PATH = str(Path(__file__).resolve().parent.parent / "data" / "corpus.txt")


@pytest.fixture(scope="module")
def ir_components():
    index = ClothingCorpusIndex(CORPUS_PATH)
    vsm = VSMRetriever(index)
    spelling = SpellingService(index)
    thesaurus = ClothingThesaurusService(index)
    return {
        "index": index,
        "vsm": vsm,
        "spelling": spelling,
        "thesaurus": thesaurus
    }


def test_spelling_correction_coton_shit(ir_components):
    spelling = ir_components["spelling"]
    result = spelling.correct_query("coton shit")
    assert result["was_corrected"] is True
    assert result["corrected_query"] == "cotton shirt"
    assert result["corrections"]["coton"] == "cotton"
    assert result["corrections"]["shit"] == "shirt"


def test_spelling_correction_hoddie(ir_components):
    spelling = ir_components["spelling"]
    result = spelling.correct_query("hoddie")
    assert result["was_corrected"] is True
    assert result["corrected_query"] == "hoodie"
    assert result["corrections"]["hoddie"] == "hoodie"


def test_spelling_correction_sweter(ir_components):
    spelling = ir_components["spelling"]
    result = spelling.correct_query("sweter")
    assert result["was_corrected"] is True
    assert result["corrected_query"] == "sweater"


def test_synonym_expansion_hoodie(ir_components):
    thesaurus = ir_components["thesaurus"]
    result = thesaurus.expand_query("hoodie")
    assert result["has_expansions"] is True
    assert "sweatshirt" in result["expanded_terms"]
    assert "sweater" in result["expanded_terms"]
    # Primary term has weight 1.0, synonyms have weight ~0.55
    assert result["term_weights"]["hoodie"] == 1.0
    assert result["term_weights"]["sweatshirt"] == 0.55


def test_synonym_expansion_sweater(ir_components):
    thesaurus = ir_components["thesaurus"]
    result = thesaurus.expand_query("sweater")
    assert result["has_expansions"] is True
    assert "sweatshirt" in result["expanded_terms"]
    assert "hoodie" in result["expanded_terms"]


def test_handle_vsm_search_coton_shit():
    res = handle_vsm_search("coton shit", top_k=10, corpus_path=CORPUS_PATH)
    assert res["success"] is True
    assert res["was_corrected"] is True
    assert res["suggested_query"] == "cotton shirt"
    assert res["total_results"] > 0
    # Top results should be shirts or t-shirts
    top_categories = [r["category"] for r in res["results"][:5]]
    assert any(cat in ("Shirt", "T-Shirt") for cat in top_categories)


def test_handle_vsm_search_hoddie_retrieves_sweatshirt_and_hoodie():
    res = handle_vsm_search("hoddie", top_k=20, corpus_path=CORPUS_PATH)
    assert res["success"] is True
    assert res["was_corrected"] is True
    assert res["suggested_query"] == "hoodie"
    assert res["total_results"] >= 10

    # Ranks 1-10 are exact Hoodies
    for r in res["results"][:10]:
        assert r["category"] == "Hoodie"

    # Subsequent ranks include Sweatshirts (sweater category in corpus)
    categories_11_to_20 = [r["category"] for r in res["results"][10:20]]
    assert "Sweatshirt" in categories_11_to_20


def test_handle_vsm_search_sweater():
    # The term 'sweater' does not literally appear in the 100 docs,
    # but through synonym expansion it surfaces sweatshirts and hoodies
    res = handle_vsm_search("sweater", top_k=10, corpus_path=CORPUS_PATH)
    assert res["success"] is True
    assert res["total_results"] > 0
    categories = [r["category"] for r in res["results"]]
    assert any(cat in ("Sweatshirt", "Hoodie") for cat in categories)


def test_handle_vsm_search_wmen_top_no_men_apparel():
    """
    Critical Bug Fix Verification:
    Searching 'wmen top' must auto-correct 'wmen' -> 'women', detect gender intent 'women',
    and MUST NOT show Men's apparel. All returned documents must be Women's or Unisex.
    """
    res = handle_vsm_search("wmen top", top_k=10, corpus_path=CORPUS_PATH)
    assert res["success"] is True
    assert res["was_corrected"] is True
    assert "women" in res["effective_query"].lower()
    assert res["gender_intent"] == "women"
    assert res["total_results"] > 0

    # Ensure EVERY single returned garment is Women's (or Unisex), strictly ZERO Men's garments
    for r in res["results"]:
        title = r["title"]
        assert title.startswith(("Women's", "Unisex")), f"Found Men's garment in women search: {title}"
        assert "Men's" not in title


def test_handle_vsm_search_men_top_no_women_apparel():
    """
    Searching 'men top' must detect gender intent 'men' and only return Men's or Unisex apparel.
    """
    res = handle_vsm_search("men top", top_k=10, corpus_path=CORPUS_PATH)
    assert res["success"] is True
    assert res["gender_intent"] == "men"
    assert res["total_results"] > 0

    for r in res["results"]:
        title = r["title"]
        assert title.startswith(("Men's", "Unisex")), f"Found Women's garment in men search: {title}"
        assert "Women's" not in title


def test_neutral_query_no_gender_intent():
    """
    Neutral queries like 'cotton shirt' should not enforce gender filtering.
    """
    res = handle_vsm_search("cotton shirt", top_k=10, corpus_path=CORPUS_PATH)
    assert res["success"] is True
    assert res["gender_intent"] is None
    assert res["total_results"] > 0

