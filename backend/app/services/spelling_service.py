"""
Spelling Correction & Typo Tolerance Service
============================================
Provides fast, corpus-aware spelling correction for clothing search queries.
Uses Levenshtein / Damerau-Levenshtein distance weighted by corpus word frequency.
"""

import re
import difflib
from collections import Counter
from typing import Dict, List, Tuple, Any, Optional


class SpellingService:
    """
    Spelling Corrector tailored to the clothing corpus and fashion domain vocabulary.
    """

    # Core fashion / clothing domain vocabulary with high baseline frequency
    DOMAIN_VOCABULARY = {
        # Garment types & categories
        "cotton": 150, "shirt": 120, "hoodie": 100, "sweatshirt": 100, "sweater": 80,
        "jacket": 100, "kurta": 100, "saree": 100, "denim": 100, "jeans": 100,
        "dress": 100, "leggings": 100, "tshirt": 100, "top": 80, "pullover": 60,
        "cardigan": 50, "trousers": 60, "pants": 60, "blazer": 50, "coat": 50,
        "fleece": 80, "puffer": 50, "midi": 50, "chiffon": 50, "handloom": 50,
        "spandex": 40, "nylon": 40, "polyester": 50,
        # Colors & styling
        "black": 90, "white": 90, "blue": 90, "navy": 80, "maroon": 80, "olive": 80,
        "yellow": 70, "grey": 70, "gray": 70, "beige": 70, "wine": 70, "green": 70,
        "casual": 80, "checked": 60, "printed": 60, "solid": 60, "oversized": 50,
        "slim": 50, "regular": 50, "winter": 60, "festive": 60, "everyday": 70,
        "comfortable": 60, "stretch": 60, "unisex": 50, "mens": 60, "womens": 60
    }

    # Common typo direct mappings for instant O(1) resolution
    KNOWN_MISSPELLINGS = {
        "coton": "cotton",
        "cotten": "cotton",
        "shit": "shirt",
        "shrt": "shirt",
        "wmen": "women",
        "wmn": "women",
        "woman": "women",
        "womans": "women",
        "womem": "women",
        "meen": "men",
        "mns": "men",
        "hoddie": "hoodie",
        "hodi": "hoodie",
        "hoody": "hoodie",
        "sweter": "sweater",
        "swetter": "sweater",
        "sweatshrt": "sweatshirt",
        "sweatshit": "sweatshirt",
        "jaket": "jacket",
        "jackt": "jacket",
        "jeens": "jeans",
        "jens": "jeans",
        "denm": "denim",
        "sari": "saree",
        "kruta": "kurta",
        "dres": "dress",
        "leging": "leggings",
        "legings": "leggings",
        "flece": "fleece"
    }

    def __init__(self, index: Optional[Any] = None):
        self.vocab_counts: Counter = Counter(self.DOMAIN_VOCABULARY)
        if index and hasattr(index, "documents"):
            self._build_vocab_from_corpus(index.documents)

    def _build_vocab_from_corpus(self, documents: Dict[str, Any]):
        """Extracts and tallies unstemmed vocabulary from the actual document corpus."""
        for doc in documents.values():
            text = f"{getattr(doc, 'category', '')} {getattr(doc, 'title', '')} {getattr(doc, 'text', '')}"
            words = re.findall(r"[a-zA-Z]+", text.lower())
            for w in words:
                if len(w) >= 2:
                    self.vocab_counts[w] += 1

    def correct_word(self, word: str) -> Tuple[str, bool]:
        """
        Corrects a single word if it is misspelled.
        Returns (corrected_word, was_changed).
        """
        w_low = word.lower()

        # Special case: 'shit' is an English word but in clothing context it's always a typo for 'shirt'
        if w_low == "shit":
            return "shirt", True

        # 1. Exact match in vocabulary
        if w_low in self.vocab_counts and self.vocab_counts[w_low] > 0:
            return word, False

        # 2. Known dictionary mappings
        if w_low in self.KNOWN_MISSPELLINGS:
            target = self.KNOWN_MISSPELLINGS[w_low]
            if word.isupper():
                return target.upper(), True
            elif word.istitle():
                return target.capitalize(), True
            return target, True

        # 3. Fuzzy match candidates via SequenceMatcher (edit distance heuristic)
        candidates = difflib.get_close_matches(w_low, list(self.vocab_counts.keys()), n=5, cutoff=0.65)
        if candidates:
            candidates.sort(
                key=lambda c: (
                    -difflib.SequenceMatcher(None, w_low, c).ratio(),
                    -self.vocab_counts[c]
                )
            )
            best_match = candidates[0]
            if word.isupper():
                return best_match.upper(), True
            elif word.istitle():
                return best_match.capitalize(), True
            return best_match, True

        return word, False

    def correct_query(self, query: str) -> Dict[str, Any]:
        """
        Corrects all words in a query string.
        Returns a dictionary with correction metadata.
        """
        raw_query = query.strip()
        if not raw_query:
            return {
                "original_query": query,
                "corrected_query": query,
                "was_corrected": False,
                "corrections": {}
            }

        tokens = re.findall(r"[a-zA-Z0-9]+|[^a-zA-Z0-9\s]+|\s+", raw_query)
        corrected_tokens = []
        corrections = {}
        was_corrected = False

        for tok in tokens:
            if re.match(r"^[a-zA-Z]+$", tok):
                corrected, changed = self.correct_word(tok)
                if changed:
                    corrections[tok] = corrected
                    was_corrected = True
                corrected_tokens.append(corrected)
            else:
                corrected_tokens.append(tok)

        corrected_query = "".join(corrected_tokens)

        return {
            "original_query": raw_query,
            "corrected_query": corrected_query,
            "was_corrected": was_corrected,
            "corrections": corrections
        }
