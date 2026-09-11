"""
Inverted Index and Positional Index Service (CSD358)
====================================================
Constructs and serializes both standard inverted index and positional index.
Precomputes document lengths for lnc.ltc cosine normalization.
"""

import os
import re
import math
import json
from typing import Dict, List, Tuple, Any
from .preprocessor import Preprocessor
from ..models.document import Document


class ClothingCorpusIndex:
    """
    Builds, manages, and serializes the Inverted Index and Positional Index.
    """

    def __init__(self, corpus_path: str = None):
        self.preprocessor = Preprocessor()
        self.documents: Dict[str, Document] = {}
        self.inverted_index: Dict[str, Dict[str, Any]] = {}  # term -> {"df": int, "postings": [(docID, tf)]}
        self.positional_index: Dict[str, Dict[str, Any]] = {}  # term -> {"df": int, "postings": [(docID, tf, [p1, p2...])]}
        self.vocabulary: List[str] = []
        self.total_docs: int = 0

        if corpus_path:
            self.load_corpus(corpus_path)
            self.build_indices()

    def load_corpus(self, corpus_path: str):
        """Parses documents enclosed in <DOC> ... </DOC> tags from the file."""
        if not os.path.exists(corpus_path):
            raise FileNotFoundError(f"Corpus file not found: {corpus_path}")

        with open(corpus_path, "r", encoding="utf-8") as f:
            content = f.read()

        doc_pattern = re.compile(r'<DOC>(.*?)</DOC>', re.DOTALL)
        matches = doc_pattern.findall(content)

        for match in matches:
            doc_id_match = re.search(r'<DOCID>(.*?)</DOCID>', match)
            category_match = re.search(r'<CATEGORY>(.*?)</CATEGORY>', match)
            title_match = re.search(r'<TITLE>(.*?)</TITLE>', match)
            text_match = re.search(r'<TEXT>(.*?)</TEXT>', match)

            if doc_id_match and category_match and title_match and text_match:
                doc_id = doc_id_match.group(1).strip()
                category = category_match.group(1).strip()
                title = title_match.group(1).strip()
                text = text_match.group(1).strip()

                doc = Document(doc_id, category, title, text)
                self.documents[doc_id] = doc

        self.total_docs = len(self.documents)

    def build_indices(self):
        """Processes all documents and populates inverted and positional indices."""
        temp_postings: Dict[str, Dict[str, List[int]]] = {}

        for doc_id, doc in self.documents.items():
            doc.tokens = self.preprocessor.preprocess_tokens_with_positions(doc.combined_text)
            doc.tf_dict = {}
            doc.positions_dict = {}
            doc.char_spans_dict = {}

            for term, pos, start_char, end_char in doc.tokens:
                doc.tf_dict[term] = doc.tf_dict.get(term, 0) + 1
                if term not in doc.positions_dict:
                    doc.positions_dict[term] = []
                    doc.char_spans_dict[term] = []
                doc.positions_dict[term].append(pos)
                doc.char_spans_dict[term].append((start_char, end_char))

                if term not in temp_postings:
                    temp_postings[term] = {}
                if doc_id not in temp_postings[term]:
                    temp_postings[term][doc_id] = []
                temp_postings[term][doc_id].append(pos)

            # Precompute document length for lnc weighting: sqrt(sum((1 + log10(tf))^2))
            sum_sq = 0.0
            for term, tf in doc.tf_dict.items():
                w_d = 1.0 + math.log10(tf)
                sum_sq += w_d * w_d
            doc.vector_length = math.sqrt(sum_sq) if sum_sq > 0 else 1.0

        # Build final sorted dictionary & postings
        self.vocabulary = sorted(temp_postings.keys())
        self.inverted_index = {}
        self.positional_index = {}

        for term in self.vocabulary:
            doc_dict = temp_postings[term]
            df = len(doc_dict)
            sorted_doc_ids = sorted(doc_dict.keys())

            inv_postings = []
            pos_postings = []

            for doc_id in sorted_doc_ids:
                positions = sorted(doc_dict[doc_id])
                tf = len(positions)
                inv_postings.append((doc_id, tf))
                pos_postings.append((doc_id, tf, positions))

            self.inverted_index[term] = {
                "df": df,
                "postings": inv_postings
            }
            self.positional_index[term] = {
                "df": df,
                "postings": pos_postings
            }

    def save_indices(self, output_dir: str):
        """Serializes dictionary/inverted-index and positional-index into both JSON and formatted TXT files."""
        os.makedirs(output_dir, exist_ok=True)

        inv_json_path = os.path.join(output_dir, "inverted_index.json")
        pos_json_path = os.path.join(output_dir, "positional_index.json")
        inv_txt_path = os.path.join(output_dir, "inverted_index.txt")
        pos_txt_path = os.path.join(output_dir, "positional_index.txt")

        # Save Inverted Index JSON
        with open(inv_json_path, "w", encoding="utf-8") as f:
            json.dump(self.inverted_index, f, indent=2)

        # Save Positional Index JSON
        with open(pos_json_path, "w", encoding="utf-8") as f:
            json.dump(self.positional_index, f, indent=2)

        # Save Formatted Inverted Index TXT
        with open(inv_txt_path, "w", encoding="utf-8") as f:
            f.write(f"CSD358 Inverted Index (Dictionary)\n")
            f.write(f"Total Vocabulary Size: {len(self.vocabulary)} terms | Total Documents: {self.total_docs}\n")
            f.write(f"{'='*80}\n\n")
            for term in self.vocabulary:
                entry = self.inverted_index[term]
                postings_str = ", ".join([f"({doc_id}, tf={tf})" for doc_id, tf in entry["postings"]])
                f.write(f"{term:<20} [df={entry['df']:<3}] -> {postings_str}\n")

        # Save Formatted Positional Index TXT
        with open(pos_txt_path, "w", encoding="utf-8") as f:
            f.write(f"CSD358 Positional Inverted Index\n")
            f.write(f"Total Vocabulary Size: {len(self.vocabulary)} terms | Total Documents: {self.total_docs}\n")
            f.write(f"{'='*80}\n\n")
            for term in self.vocabulary:
                entry = self.positional_index[term]
                postings_str = "; ".join([f"{doc_id} [tf={tf}: {positions}]" for doc_id, tf, positions in entry["postings"]])
                f.write(f"{term:<20} [df={entry['df']:<3}] -> {postings_str}\n")
