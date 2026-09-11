"""
Positional Search Module (CSD358)
=================================
Implements Part C requirements:
1. Exact Phrase Search:
   Finds documents where query terms occur at strictly consecutive token positions:
   pos(t_{i+1}) = pos(t_i) + 1
2. Ordered Proximity Search:
   Finds documents where two query terms occur within k token positions:
   0 < pos(t2) - pos(t1) <= k (e.g. 'cotton WITHIN/3 shirt')
3. Evidence Generation:
   Returns matching position lists and token spans for visual verification in the UI.
"""

import re
from typing import List, Dict, Tuple, Any, Optional
from .indexer import ClothingCorpusIndex
from .preprocessor import Preprocessor


class PositionalSearcher:
    """
    Executes exact phrase and ordered proximity searches using positional postings.
    """

    def __init__(self, index: ClothingCorpusIndex):
        self.index = index
        self.preprocessor = Preprocessor()

    def get_term_postings_map(self, term: str) -> Dict[str, List[int]]:
        """Returns map of doc_id -> list of positions for a stemmed term."""
        if term not in self.index.positional_index:
            return {}
        return {doc_id: positions for doc_id, tf, positions in self.index.positional_index[term]["postings"]}

    def search_exact_phrase(self, phrase: str) -> List[Dict[str, Any]]:
        """
        Executes exact phrase search: consecutive positions p_{i+1} = p_i + 1.
        Returns list of matching documents with match positions.
        """
        clean_phrase = phrase.strip().strip('"').strip("'")
        terms = self.preprocessor.preprocess(clean_phrase)
        if not terms:
            return []

        # If phrase contains only 1 term, return all docs with that term
        if len(terms) == 1:
            term = terms[0]
            if term not in self.index.positional_index:
                return []
            results = []
            for doc_id, tf, positions in self.index.positional_index[term]["postings"]:
                doc = self.index.documents[doc_id]
                results.append({
                    "doc_id": doc_id,
                    "category": doc.category,
                    "title": doc.title,
                    "text": doc.text,
                    "match_count": len(positions),
                    "matched_positions": [[p] for p in positions],
                    "query_terms": terms
                })
            return sorted(results, key=lambda x: x["doc_id"])

        # Multiple terms: check consecutive positions across postings
        first_term = terms[0]
        current_matches: Dict[str, List[List[int]]] = {}

        if first_term not in self.index.positional_index:
            return []

        for doc_id, tf, positions in self.index.positional_index[first_term]["postings"]:
            current_matches[doc_id] = [[p] for p in positions]

        for i in range(1, len(terms)):
            term = terms[i]
            if term not in self.index.positional_index:
                return []
            next_postings = self.get_term_postings_map(term)
            new_matches: Dict[str, List[List[int]]] = {}

            for doc_id, chains in current_matches.items():
                if doc_id not in next_postings:
                    continue
                doc_positions = next_postings[doc_id]
                valid_chains = []
                for chain in chains:
                    last_pos = chain[-1]
                    expected_pos = last_pos + 1
                    if expected_pos in doc_positions:
                        valid_chains.append(chain + [expected_pos])
                if valid_chains:
                    new_matches[doc_id] = valid_chains

            current_matches = new_matches

        results = []
        for doc_id in sorted(current_matches.keys()):
            doc = self.index.documents[doc_id]
            chains = current_matches[doc_id]
            results.append({
                "doc_id": doc_id,
                "category": doc.category,
                "title": doc.title,
                "text": doc.text,
                "match_count": len(chains),
                "matched_positions": chains,
                "query_terms": terms
            })

        return results

    def search_proximity(self, term1_raw: str, term2_raw: str, k: int) -> List[Dict[str, Any]]:
        """
        Executes ordered proximity search: 0 < pos(t2) - pos(t1) <= k.
        Returns matching documents with matching position pairs (p1, p2).
        """
        term1_list = self.preprocessor.preprocess(term1_raw)
        term2_list = self.preprocessor.preprocess(term2_raw)

        if not term1_list or not term2_list:
            return []

        t1 = term1_list[0]
        t2 = term2_list[0]

        if t1 not in self.index.positional_index or t2 not in self.index.positional_index:
            return []

        postings1 = self.get_term_postings_map(t1)
        postings2 = self.get_term_postings_map(t2)

        common_doc_ids = sorted(set(postings1.keys()) & set(postings2.keys()))
        results = []

        for doc_id in common_doc_ids:
            pos_list1 = postings1[doc_id]
            pos_list2 = postings2[doc_id]

            # Find pairs where 0 < p2 - p1 <= k
            matched_pairs = []
            for p1 in pos_list1:
                for p2 in pos_list2:
                    diff = p2 - p1
                    if 0 < diff <= k:
                        matched_pairs.append((p1, p2, diff))

            if matched_pairs:
                doc = self.index.documents[doc_id]
                results.append({
                    "doc_id": doc_id,
                    "category": doc.category,
                    "title": doc.title,
                    "text": doc.text,
                    "match_count": len(matched_pairs),
                    "matched_pairs": matched_pairs,  # [(p1, p2, distance), ...]
                    "query_terms": [t1, t2],
                    "k": k
                })

        return sorted(results, key=lambda x: x["doc_id"])

    def parse_and_search(self, query_str: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Detects query syntax:
        - "term1 WITHIN/k term2" -> Proximity Search
        - Quotes ("cotton shirt") -> Phrase Search
        - Fallback -> Exact phrase search on all tokens
        """
        query_str = query_str.strip()

        # Check for WITHIN/k pattern
        within_match = re.search(r'([A-Za-z0-9]+)\s+WITHIN/(\d+)\s+([A-Za-z0-9]+)', query_str, re.IGNORECASE)
        if within_match:
            t1 = within_match.group(1)
            k = int(within_match.group(2))
            t2 = within_match.group(3)
            return "proximity", self.search_proximity(t1, t2, k)

        # Exact phrase search
        return "phrase", self.search_exact_phrase(query_str)
