"""
Semantic Search Service (Embedding-based Neural IR)
===================================================
Feature Innovation #4 for CSD358 Clothing Search Engine.

Uses `all-MiniLM-L6-v2` (via sentence-transformers) to map product descriptions
and natural language queries into a unified 384-dimensional dense semantic space.
Supports:
1. Pure dense semantic retrieval via cosine similarity.
2. Natural Language query intent detection (conversational marker heuristics).
3. Hybrid alpha-blended retrieval (Semantic + Lexical lnc.ltc VSM).
"""

import os
import pickle
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SentenceTransformer = None
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class SemanticSearchService:
    """
    Embedding-based semantic retrieval engine using all-MiniLM-L6-v2.
    """

    MODEL_NAME = "all-MiniLM-L6-v2"
    DEFAULT_INDEX_FILENAME = "semantic_index.pkl"

    def __init__(self, index_path: Optional[str] = None, model: Optional[Any] = None):
        self._model = model
        self.index_path = index_path
        self.doc_ids: List[str] = []
        self.metadata: Dict[str, Dict[str, str]] = {}
        self.embeddings: Optional[np.ndarray] = None
        self.is_loaded: bool = False

        if index_path and os.path.exists(index_path):
            self.load_index(index_path)

    @property
    def model(self):
        """Lazy loader for the SentenceTransformer model to optimize cold start."""
        if self._model is None:
            if not SENTENCE_TRANSFORMERS_AVAILABLE:
                raise RuntimeError(
                    "sentence-transformers is not installed. Run `.venv/bin/pip install sentence-transformers`."
                )
            self._model = SentenceTransformer(self.MODEL_NAME)
        return self._model

    def build_index(self, documents: Dict[str, Any], save_path: Optional[str] = None) -> np.ndarray:
        """
        Encodes document corpus into 384-dim normalized dense vectors and serializes the index.
        """
        self.doc_ids = sorted(list(documents.keys()))
        self.metadata = {}
        texts_to_encode = []

        for doc_id in self.doc_ids:
            doc = documents[doc_id]
            title = getattr(doc, "title", "")
            category = getattr(doc, "category", "")
            text = getattr(doc, "text", "")
            combined = getattr(doc, "combined_text", f"{title}. {text}")

            self.metadata[doc_id] = {
                "category": category,
                "title": title,
                "text": text,
                "combined_text": combined
            }
            # Enrich document text with explicit category context for superior semantic matching
            enriched_text = f"Category: {category}. Product: {title}. Description: {text}"
            texts_to_encode.append(enriched_text)

        # Batch encode with L2 normalization (cosine similarity = dot product)
        raw_embeddings = self.model.encode(
            texts_to_encode,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        self.embeddings = np.array(raw_embeddings, dtype=np.float32)
        self.is_loaded = True

        if save_path:
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            payload = {
                "model_name": self.MODEL_NAME,
                "embedding_dim": int(self.embeddings.shape[1]),
                "doc_ids": self.doc_ids,
                "metadata": self.metadata,
                "embeddings": self.embeddings
            }
            with open(save_path, "wb") as f:
                pickle.dump(payload, f, protocol=pickle.HIGHEST_PROTOCOL)
            self.index_path = save_path

        return self.embeddings

    def load_index(self, save_path: str):
        """Loads precomputed embeddings and metadata from pickle artifact."""
        if not os.path.exists(save_path):
            raise FileNotFoundError(f"Semantic index not found at: {save_path}")

        with open(save_path, "rb") as f:
            data = pickle.load(f)

        self.doc_ids = data["doc_ids"]
        self.metadata = data["metadata"]
        self.embeddings = np.array(data["embeddings"], dtype=np.float32)
        self.index_path = save_path
        self.is_loaded = True

    @staticmethod
    def is_natural_language(query: str) -> bool:
        """
        Determines whether a query is conversational/natural language or keyword-style.
        Checks for semantic markers and length threshold.
        """
        tokens = query.lower().strip().split()
        if len(tokens) >= 5:
            return True

        nl_markers = {
            "who", "what", "which", "where", "how", "why",
            "for", "with", "without", "under", "best", "good",
            "comfortable", "warm", "suitable", "perfect", "look",
            "looking", "need", "want", "ideal", "wearable"
        }
        return any(t in nl_markers for t in tokens)

    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Performs pure dense semantic retrieval for the query.
        """
        if not self.is_loaded or self.embeddings is None:
            raise RuntimeError("Semantic index is not loaded. Call build_index() or load_index().")

        q_clean = query.strip()
        if not q_clean:
            return []

        # Encode query to 384-dim normalized vector
        q_vec = self.model.encode([q_clean], normalize_embeddings=True, show_progress_bar=False)[0]
        q_vec = np.array(q_vec, dtype=np.float32)

        # Dot product with pre-normalized embeddings gives exact cosine similarity in [-1, 1]
        scores = self.embeddings @ q_vec

        # Top-k ranking
        ranked_indices = np.argsort(-scores)[:top_k]

        results = []
        for rank, idx in enumerate(ranked_indices, start=1):
            doc_id = self.doc_ids[idx]
            meta = self.metadata.get(doc_id, {})
            score = float(scores[idx])

            results.append({
                "rank": rank,
                "doc_id": doc_id,
                "category": meta.get("category", ""),
                "title": meta.get("title", ""),
                "text": meta.get("text", ""),
                "semantic_score": round(score, 6),
                "combined_score": round(score, 6)
            })

        return results

    def hybrid_search(
        self,
        query: str,
        vsm_retriever: Any,
        alpha: float = 0.5,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Combines semantic similarity with lexical lnc.ltc VSM score:
        Combined_Score = alpha * Score_semantic + (1 - alpha) * Score_lexical

        alpha = 1.0 -> Pure semantic search
        alpha = 0.0 -> Pure lexical VSM search
        alpha = 0.5 -> Balanced hybrid search
        """
        if not self.is_loaded or self.embeddings is None:
            raise RuntimeError("Semantic index is not loaded. Call build_index() or load_index().")

        q_clean = query.strip()
        if not q_clean:
            return []

        # 1. Compute semantic scores for all documents
        q_vec = self.model.encode([q_clean], normalize_embeddings=True, show_progress_bar=False)[0]
        q_vec = np.array(q_vec, dtype=np.float32)
        sem_scores_array = self.embeddings @ q_vec
        sem_scores: Dict[str, float] = {
            self.doc_ids[i]: float(sem_scores_array[i]) for i in range(len(self.doc_ids))
        }

        # 2. Compute lexical VSM scores
        vsm_results = vsm_retriever.search(q_clean, top_k=len(self.doc_ids))
        lex_scores: Dict[str, float] = {
            r["doc_id"]: r["cosine_score"] for r in vsm_results
        }

        # 3. Blend scores across documents
        # Candidate set: documents matching either lexical OR having top semantic score
        combined_scores: Dict[str, Dict[str, float]] = {}
        for doc_id in self.doc_ids:
            s_score = max(0.0, sem_scores.get(doc_id, 0.0))  # Clamp negative cosine similarities
            l_score = lex_scores.get(doc_id, 0.0)

            blended = (alpha * s_score) + ((1.0 - alpha) * l_score)
            combined_scores[doc_id] = {
                "combined": blended,
                "semantic": s_score,
                "lexical": l_score
            }

        # Sort primarily by blended score descending, secondary by doc_id ascending
        sorted_doc_ids = sorted(
            combined_scores.keys(),
            key=lambda d_id: (-round(combined_scores[d_id]["combined"], 6), d_id)
        )

        results = []
        for rank, doc_id in enumerate(sorted_doc_ids[:top_k], start=1):
            meta = self.metadata.get(doc_id, {})
            score_data = combined_scores[doc_id]

            results.append({
                "rank": rank,
                "doc_id": doc_id,
                "category": meta.get("category", ""),
                "title": meta.get("title", ""),
                "text": meta.get("text", ""),
                "combined_score": round(score_data["combined"], 6),
                "semantic_score": round(score_data["semantic"], 6),
                "lexical_score": round(score_data["lexical"], 6),
                "alpha": round(alpha, 2)
            })

        return results
