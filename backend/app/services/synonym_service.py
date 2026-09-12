"""
Clothing Synonym & Query Expansion Service
==========================================
Bridges the vocabulary gap in fashion Information Retrieval (e.g. 'hoodie' <-> 'sweater'/'sweatshirt').
Expands queries with domain synonyms using calibrated weights to rank exact matches first
while seamlessly surfacing conceptually related apparel.
"""

import re
from typing import Dict, List, Tuple, Any, Optional, Set


class ClothingThesaurusService:
    """
    Fashion and apparel domain thesaurus with query expansion capabilities.
    """

    APPAREL_SYNONYMS: Dict[str, List[str]] = {
        # Winter tops & fleece wear
        "hoodie": ["sweatshirt", "sweater", "pullover", "fleece"],
        "sweater": ["sweatshirt", "hoodie", "pullover", "cardigan", "fleece"],
        "sweatshirt": ["hoodie", "sweater", "pullover", "fleece"],
        "pullover": ["hoodie", "sweatshirt", "sweater"],
        "cardigan": ["sweater", "sweatshirt", "jacket"],
        "fleece": ["hoodie", "sweatshirt", "jacket", "warm"],

        # Shirts & Tops
        "shirt": ["t-shirt", "tshirt", "top", "kurta", "tunic"],
        "t-shirt": ["shirt", "tee", "top"],
        "tshirt": ["shirt", "tee", "top"],
        "tee": ["t-shirt", "shirt", "top"],
        "top": ["shirt", "t-shirt", "tunic"],
        "kurta": ["tunic", "ethnic", "shirt"],
        "tunic": ["kurta", "top", "shirt"],

        # Bottoms & Denims
        "jeans": ["denim", "trousers", "pants"],
        "denim": ["jeans", "trousers", "pants"],
        "pants": ["jeans", "trousers", "leggings"],
        "trousers": ["pants", "jeans"],
        "leggings": ["tights", "pants", "stretch"],
        "tights": ["leggings", "pants"],

        # Outerwear
        "jacket": ["coat", "puffer", "blazer", "windbreaker", "winter wear"],
        "coat": ["jacket", "puffer", "blazer"],
        "puffer": ["jacket", "coat", "winter"],
        "blazer": ["jacket", "coat"],

        # Ethnic & Dresses
        "saree": ["sari", "handloom", "ethnic"],
        "sari": ["saree", "handloom", "ethnic"],
        "dress": ["midi", "gown", "frock"],
        "gown": ["dress", "frock"],
        "midi": ["dress"],

        # Fabrics & Attributes
        "cotton": ["cotton blend", "poly cotton"],
        "winter": ["jacket", "hoodie", "sweatshirt", "fleece"]
    }

    def __init__(self, index: Optional[Any] = None):
        self.index = index

    def get_synonyms(self, term: str) -> List[str]:
        """Returns direct synonym list for a term if available."""
        return self.APPAREL_SYNONYMS.get(term.lower(), [])

    def expand_query(
        self,
        query: str,
        primary_weight: float = 1.0,
        synonym_weight: float = 0.55,
        max_synonyms_per_term: int = 3
    ) -> Dict[str, Any]:
        """
        Expands a user query with apparel synonyms.
        Returns:
            - expanded_query_str: expanded query string (e.g. 'hoodie sweatshirt pullover')
            - term_weights: dictionary of term -> weight multiplier
            - synonym_map: dict of original query word -> list of added synonyms
            - has_expansions: bool
        """
        raw_words = re.findall(r"[a-zA-Z]+", query.lower())
        if not raw_words:
            return {
                "original_query": query,
                "expanded_query_str": query,
                "term_weights": {},
                "synonym_map": {},
                "has_expansions": False,
                "expanded_terms": []
            }

        term_weights: Dict[str, float] = {}
        synonym_map: Dict[str, List[str]] = {}
        added_synonyms: Set[str] = set()

        # 1. Add primary terms with full weight
        for word in raw_words:
            term_weights[word] = max(term_weights.get(word, 0.0), primary_weight)

        # 2. Add synonyms with calibrated secondary weight
        for word in raw_words:
            syns = self.APPAREL_SYNONYMS.get(word, [])
            valid_syns = []
            for syn in syns[:max_synonyms_per_term]:
                # Split multi-word synonyms like 'winter wear'
                subterms = syn.split()
                for st in subterms:
                    if st not in raw_words and st not in added_synonyms:
                        term_weights[st] = synonym_weight
                        added_synonyms.add(st)
                        valid_syns.append(st)
            if valid_syns:
                synonym_map[word] = valid_syns

        # 3. Construct expanded query string
        expanded_query_terms = list(raw_words) + list(added_synonyms)
        expanded_query_str = " ".join(expanded_query_terms)

        return {
            "original_query": query,
            "expanded_query_str": expanded_query_str,
            "term_weights": term_weights,
            "synonym_map": synonym_map,
            "has_expansions": len(added_synonyms) > 0,
            "expanded_terms": list(added_synonyms)
        }
