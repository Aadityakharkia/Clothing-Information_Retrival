"""
Advanced Information Retrieval Innovations Module (CSD358)
===========================================================
Implements 3 Unique Special Ideas in Information Retrieval:

1. Special Idea 1: Positional-Aware Hybrid Re-Ranking (Dynamic Proximity Boost)
   - Integrates positional shortest covering span into VSM cosine scores.
   - Clustered query terms receive a proximity bonus: Score_hybrid = Score_vsm * (1 + lambda * (|Q| / span)).

2. Special Idea 2: Interactive Positional Intersection Algorithm Trace
   - Simulates and exposes the step-by-step postings merge and positional intersection
     (Manning et al., Introduction to Information Retrieval, Ch. 2.4).
   - Returns pointer steps, document intersections, and token-level positional evidence.

3. Special Idea 3: Relevance Feedback & Pseudo-Relevance Feedback (Rocchio Engine)
   - Implements vector-space Rocchio query reformulation:
     q_m = alpha * q_0 + (beta / |Dr|) * sum(d in Dr) - (gamma / |Dnr|) * sum(d in Dnr)
   - Computes query vector drift, discovers expanded fashion attributes, and re-ranks catalog.
"""

import math
from typing import List, Dict, Tuple, Any, Optional
from .indexer import ClothingCorpusIndex
from .vsm import VSMRetriever
from .preprocessor import Preprocessor


class AdvancedIREngine:
    """
    Houses the 3 Unique Special Information Retrieval Innovations.
    """

    def __init__(self, index: ClothingCorpusIndex, vsm_retriever: VSMRetriever):
        self.index = index
        self.vsm_retriever = vsm_retriever
        self.preprocessor = Preprocessor()

    # -------------------------------------------------------------------------
    # SPECIAL IDEA 1: Positional-Aware Hybrid Re-Ranking (Dynamic Proximity Boost)
    # -------------------------------------------------------------------------
    def calculate_shortest_span(self, positions_by_term: List[List[int]]) -> Optional[int]:
        """
        Computes the shortest covering span containing at least one occurrence of each term.
        positions_by_term: list of sorted position lists for each matched term.
        Returns span length (max_pos - min_pos + 1).
        """
        if not positions_by_term or any(len(p) == 0 for p in positions_by_term):
            return None

        num_terms = len(positions_by_term)
        if num_terms == 1:
            return 1

        # Flatten into sorted events (pos, term_idx)
        events = []
        for term_idx, pos_list in enumerate(positions_by_term):
            for pos in pos_list:
                events.append((pos, term_idx))
        events.sort(key=lambda x: x[0])

        min_span = float("inf")
        term_counts: Dict[int, int] = {}
        left = 0

        for right in range(len(events)):
            r_pos, r_term = events[right]
            term_counts[r_term] = term_counts.get(r_term, 0) + 1

            # When all terms are present in current window
            while len(term_counts) == num_terms:
                l_pos, l_term = events[left]
                span = r_pos - l_pos + 1
                if span < min_span:
                    min_span = span

                term_counts[l_term] -= 1
                if term_counts[l_term] == 0:
                    del term_counts[l_term]
                left += 1

        return min_span if min_span != float("inf") else None

    def search_hybrid_proximity_boost(self, query: str, lambda_param: float = 0.5, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieves documents via VSM and applies Positional Proximity Boost.
        Boost = 1.0 + lambda * (num_matched_terms / shortest_span)
        """
        vsm_results = self.vsm_retriever.search(query, top_k=self.index.total_docs)
        if not vsm_results:
            return []

        query_terms = list(dict.fromkeys(self.preprocessor.preprocess(query)))
        if len(query_terms) <= 1:
            # Single term query: span boost is 1.0 (no relative proximity between terms)
            return vsm_results[:top_k]

        hybrid_results = []
        for res in vsm_results:
            doc_id = res["doc_id"]
            doc = self.index.documents[doc_id]

            # Gather positions for each query term in this document
            matched_terms = []
            term_positions_list = []
            for t in query_terms:
                if t in doc.positions_dict and len(doc.positions_dict[t]) > 0:
                    matched_terms.append(t)
                    term_positions_list.append(doc.positions_dict[t])

            if len(matched_terms) >= 2:
                shortest_span = self.calculate_shortest_span(term_positions_list)
                if shortest_span and shortest_span > 0:
                    proximity_factor = len(matched_terms) / float(shortest_span)
                    boost = 1.0 + (lambda_param * proximity_factor)
                else:
                    shortest_span = None
                    boost = 1.0
            else:
                shortest_span = None
                boost = 1.0

            hybrid_score = res["cosine_score"] * boost
            hybrid_results.append({
                **res,
                "vsm_score": res["cosine_score"],
                "hybrid_score": round(hybrid_score, 6),
                "boost_factor": round(boost, 4),
                "shortest_span": shortest_span,
                "matched_terms_count": len(matched_terms)
            })

        # Sort by decreasing hybrid score; break ties by docID
        hybrid_results.sort(key=lambda x: (-x["hybrid_score"], x["doc_id"]))

        for rank, item in enumerate(hybrid_results[:top_k], start=1):
            item["rank"] = rank

        return hybrid_results[:top_k]

    # -------------------------------------------------------------------------
    # SPECIAL IDEA 2: Interactive Postings & Positional Intersection Trace Visualizer
    # -------------------------------------------------------------------------
    def trace_positional_intersect(self, term1_raw: str, term2_raw: str, k: int = 1) -> Dict[str, Any]:
        """
        Executes and records the step-by-step Positional Intersect algorithm
        (Manning et al., Ch. 2.4).
        Generates algorithm execution logs and matched documents with token offsets.
        """
        t1_terms = self.preprocessor.preprocess(term1_raw)
        t2_terms = self.preprocessor.preprocess(term2_raw)

        if not t1_terms or not t2_terms:
            return {"error": "Invalid or stopped terms provided"}

        t1 = t1_terms[0]
        t2 = t2_terms[0]

        postings1 = self.index.positional_index.get(t1, {"postings": []})["postings"]
        postings2 = self.index.positional_index.get(t2, {"postings": []})["postings"]

        trace_log = []
        matches = []
        p1_idx = 0
        p2_idx = 0

        trace_log.append(f"Starting Positional Intersect for '{t1}' and '{t2}' with max distance k={k}.")
        trace_log.append(f"Postings list for '{t1}': {len(postings1)} docs. Postings list for '{t2}': {len(postings2)} docs.")

        while p1_idx < len(postings1) and p2_idx < len(postings2):
            doc1, tf1, pos1 = postings1[p1_idx]
            doc2, tf2, pos2 = postings2[p2_idx]

            if doc1 == doc2:
                trace_log.append(f"Doc match found: {doc1}. Checking positional overlap (pos1={pos1}, pos2={pos2})...")
                # Positional check inside matching document
                doc_matches = []
                pp1 = 0
                pp2 = 0
                while pp1 < len(pos1):
                    while pp2 < len(pos2):
                        diff = pos2[pp2] - pos1[pp1]
                        if 0 < diff <= k:
                            doc_matches.append((pos1[pp1], pos2[pp2], diff))
                            trace_log.append(f"  -> Valid proximity: pos('{t1}')={pos1[pp1]}, pos('{t2}')={pos2[pp2]}, dist={diff} <= {k}")
                        elif pos2[pp2] > pos1[pp1]:
                            break
                        pp2 += 1
                    pp1 += 1

                if doc_matches:
                    doc = self.index.documents[doc1]
                    matches.append({
                        "doc_id": doc1,
                        "title": doc.title,
                        "category": doc.category,
                        "matched_pairs": doc_matches
                    })
                    trace_log.append(f"Document {doc1} accepted with {len(doc_matches)} match(es).")
                else:
                    trace_log.append(f"Document {doc1} rejected (no pairs within distance {k}).")

                p1_idx += 1
                p2_idx += 1
            elif doc1 < doc2:
                trace_log.append(f"Advancing '{t1}' pointer: doc {doc1} < doc {doc2}")
                p1_idx += 1
            else:
                trace_log.append(f"Advancing '{t2}' pointer: doc {doc2} < doc {doc1}")
                p2_idx += 1

        trace_log.append(f"Intersection complete. Found {len(matches)} matching document(s).")

        return {
            "term1": t1,
            "term2": t2,
            "k": k,
            "total_matches": len(matches),
            "matches": matches,
            "trace_log": trace_log[:150]  # Cap log to avoid overwhelming UI
        }

    # -------------------------------------------------------------------------
    # SPECIAL IDEA 3: Relevance Feedback & Pseudo-Relevance Feedback (Rocchio)
    # -------------------------------------------------------------------------
    def rocchio_feedback(
        self,
        query: str,
        relevant_doc_ids: List[str],
        irrelevant_doc_ids: List[str] = None,
        alpha: float = 1.0,
        beta: float = 0.75,
        gamma: float = 0.15,
        top_expanded_terms: int = 5,
        top_k: int = 10
    ) -> Dict[str, Any]:
        """
        Implements Vector Space Rocchio Feedback:
        q_m = alpha * q_0 + (beta / |Dr|) * sum(d in Dr) - (gamma / |Dnr|) * sum(d in Dnr)
        """
        irrelevant_doc_ids = irrelevant_doc_ids or []
        norm_q_weights, q_length, _ = self.vsm_retriever.compute_query_weights(query)

        # Base query vector
        modified_vector: Dict[str, float] = {t: alpha * w for t, w in norm_q_weights.items()}

        # Accumulate relevant document vectors
        if relevant_doc_ids:
            scale_r = beta / len(relevant_doc_ids)
            for doc_id in relevant_doc_ids:
                if doc_id in self.index.documents:
                    doc = self.index.documents[doc_id]
                    for term, tf in doc.tf_dict.items():
                        w_d = (1.0 + math.log10(tf)) / doc.vector_length
                        modified_vector[term] = modified_vector.get(term, 0.0) + (scale_r * w_d)

        # Subtract irrelevant document vectors
        if irrelevant_doc_ids:
            scale_nr = gamma / len(irrelevant_doc_ids)
            for doc_id in irrelevant_doc_ids:
                if doc_id in self.index.documents:
                    doc = self.index.documents[doc_id]
                    for term, tf in doc.tf_dict.items():
                        w_d = (1.0 + math.log10(tf)) / doc.vector_length
                        modified_vector[term] = modified_vector.get(term, 0.0) - (scale_nr * w_d)

        # Remove negative weights (standard Rocchio restriction)
        modified_vector = {t: w for t, w in modified_vector.items() if w > 0.0}

        # Normalize modified query vector
        mod_length = math.sqrt(sum(w * w for w in modified_vector.values()))
        if mod_length > 0:
            for t in modified_vector:
                modified_vector[t] /= mod_length

        # Find newly expanded / highest boosted terms
        term_shifts = []
        for t, new_w in modified_vector.items():
            orig_w = norm_q_weights.get(t, 0.0)
            gain = new_w - orig_w
            term_shifts.append({"term": t, "original_weight": round(orig_w, 4), "new_weight": round(new_w, 4), "gain": round(gain, 4)})

        term_shifts.sort(key=lambda x: -x["gain"])
        top_expansions = term_shifts[:top_expanded_terms]

        # Re-rank corpus using modified vector
        doc_scores: Dict[str, float] = {}
        for term, w_q in modified_vector.items():
            if term not in self.index.inverted_index:
                continue
            for doc_id, tf in self.index.inverted_index[term]["postings"]:
                doc = self.index.documents[doc_id]
                w_d = (1.0 + math.log10(tf)) / doc.vector_length
                doc_scores[doc_id] = doc_scores.get(doc_id, 0.0) + (w_q * w_d)

        sorted_docs = sorted(doc_scores.keys(), key=lambda d: (-round(doc_scores[d], 7), d))

        reranked_results = []
        for rank, doc_id in enumerate(sorted_docs[:top_k], start=1):
            doc = self.index.documents[doc_id]
            reranked_results.append({
                "rank": rank,
                "doc_id": doc_id,
                "category": doc.category,
                "title": doc.title,
                "text": doc.text,
                "rocchio_score": round(doc_scores[doc_id], 6),
                "is_marked_relevant": doc_id in relevant_doc_ids
            })

        return {
            "original_query": query,
            "relevant_docs_count": len(relevant_doc_ids),
            "top_expanded_terms": top_expansions,
            "results": reranked_results
        }
