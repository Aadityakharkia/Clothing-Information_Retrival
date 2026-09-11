"""
Vector Space Model (VSM) Ranked Retrieval Module (CSD358)
=========================================================
Implements Part B requirements:
- Weighting scheme: lnc.ltc
  - Document (lnc): wd,t = 1 + log10(tf); no idf; cosine normalized.
  - Query (ltc): wq,t = (1 + log10(tf)) * log10(N/df) where N = 100; cosine normalized.
- Cosine similarity computation: dot product of normalized query and document vectors.
- Returns top 10 ranked documents sorted by decreasing score; ties broken by increasing docID.
"""

import math
from typing import List, Dict, Tuple, Any
from .indexer import ClothingCorpusIndex
from .preprocessor import Preprocessor


class VSMRetriever:
    """
    Ranked retrieval using the Vector Space Model with lnc.ltc weighting.
    """

    def __init__(self, index: ClothingCorpusIndex):
        self.index = index
        self.preprocessor = Preprocessor()
        self.N = index.total_docs if index.total_docs > 0 else 100

    def compute_query_weights(self, query: str) -> Tuple[Dict[str, float], float, Dict[str, Any]]:
        """
        Computes normalized query vector weights using ltc scheme:
        wq,t = (1 + log10(tf_q)) * log10(N / df)
        Length(q) = sqrt(sum(wq,t^2))
        Normalized w'q,t = wq,t / Length(q)
        """
        query_terms = self.preprocessor.preprocess(query)
        if not query_terms:
            return {}, 0.0, {}

        # Raw query term frequency
        tf_q: Dict[str, int] = {}
        for t in query_terms:
            tf_q[t] = tf_q.get(t, 0) + 1

        raw_weights: Dict[str, float] = {}
        query_details: Dict[str, Any] = {}
        sum_sq = 0.0

        for term, tf in tf_q.items():
            if term in self.index.inverted_index:
                df = self.index.inverted_index[term]["df"]
                idf = math.log10(self.N / df) if df > 0 else 0.0
            else:
                df = 0
                idf = 0.0  # Out-of-vocabulary term

            tf_weight = 1.0 + math.log10(tf)
            raw_w = tf_weight * idf
            raw_weights[term] = raw_w
            sum_sq += raw_w * raw_w

            query_details[term] = {
                "tf": tf,
                "df": df,
                "idf": idf,
                "raw_weight": raw_w
            }

        q_length = math.sqrt(sum_sq)
        norm_weights: Dict[str, float] = {}

        for term, raw_w in raw_weights.items():
            if q_length > 0:
                norm_weights[term] = raw_w / q_length
                query_details[term]["normalized_weight"] = norm_weights[term]
            else:
                norm_weights[term] = 0.0
                query_details[term]["normalized_weight"] = 0.0

        return norm_weights, q_length, query_details

    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Executes free-text VSM search using lnc.ltc cosine similarity.
        Returns top_k results with tie-breaking by increasing docID.
        """
        norm_q_weights, q_length, query_details = self.compute_query_weights(query)
        if not norm_q_weights or q_length == 0.0:
            return []

        doc_scores: Dict[str, float] = {}
        doc_term_contributions: Dict[str, Dict[str, float]] = {}

        # Accumulate dot products across matching document postings
        for term, w_prime_q in norm_q_weights.items():
            if w_prime_q == 0.0 or term not in self.index.inverted_index:
                continue

            postings = self.index.inverted_index[term]["postings"]
            for doc_id, tf in postings:
                doc = self.index.documents[doc_id]
                # Document lnc weight: (1 + log10(tf)) / doc.vector_length
                w_d = 1.0 + math.log10(tf)
                w_prime_d = w_d / doc.vector_length if doc.vector_length > 0 else 0.0

                contribution = w_prime_q * w_prime_d
                doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + contribution

                if doc_id not in doc_term_contributions:
                    doc_term_contributions[doc_id] = {}
                doc_term_contributions[doc_id][term] = contribution

        # Sort by decreasing cosine score, break ties by increasing docID
        sorted_docs = sorted(
            doc_scores.keys(),
            key=lambda d_id: (-round(doc_scores[d_id], 7), d_id)
        )

        results = []
        for rank, doc_id in enumerate(sorted_docs[:top_k], start=1):
            doc = self.index.documents[doc_id]
            results.append({
                "rank": rank,
                "doc_id": doc_id,
                "category": doc.category,
                "title": doc.title,
                "text": doc.text,
                "cosine_score": round(doc_scores[doc_id], 6),
                "term_contributions": doc_term_contributions.get(doc_id, {}),
                "vector_length": round(doc.vector_length, 4)
            })

        return results
