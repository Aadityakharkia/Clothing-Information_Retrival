"""
Autocomplete & Autofill Suggestion Service
===========================================
Provides fast, Amazon-style query autocompletion, category-scoped suggestions,
direct product matches with thumbnails, and typo tolerance.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter


CANONICAL_CATEGORY_PHOTOS = {
    'Shirt':      'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=500&q=85',
    'T-Shirt':    'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=500&q=85',
    'Jeans':      'https://images.unsplash.com/photo-1542272604-780c96856592?auto=format&fit=crop&w=500&q=85',
    'Kurta':      'https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=500&q=85',
    'Saree':      'https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=500&q=85',
    'Dress':      'https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=500&q=85',
    'Hoodie':     'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?auto=format&fit=crop&w=500&q=85',
    'Jacket':     'https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=500&q=85',
    'Leggings':   'https://images.unsplash.com/photo-1506629082955-511b1aa562c8?auto=format&fit=crop&w=500&q=85',
    'Sweatshirt': 'https://images.unsplash.com/photo-1578587018452-892bacefd3f2?auto=format&fit=crop&w=500&q=85'
}

DEFAULT_FALLBACK_PHOTO = 'https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?auto=format&fit=crop&w=500&q=85'

POPULAR_SEARCHES = [
    "Men's Cotton Crew Neck T-Shirt",
    "Regular Fit Denim Jeans",
    "Oversized Fleece Hoodie",
    "Women's Printed Daily Wear Saree",
    "Solid Cotton Midi Dress",
    "Men's Checked Cotton Shirt",
    "High Waist Stretch Leggings",
    "Casual Puffer Jacket"
]


class AutocompleteService:
    """
    In-memory autocomplete engine powered by the indexed clothing corpus.
    """

    def __init__(self, index, spelling_service=None):
        self.index = index
        self.spelling_service = spelling_service
        self.phrase_dict: Dict[str, int] = Counter()
        self.category_names: List[str] = []
        self.term_categories: Dict[str, Counter] = {}
        self.build_autocomplete_index()

    def build_autocomplete_index(self):
        """Precomputes phrases, n-grams, and category linkages from corpus documents."""
        categories = set()

        for doc_id, doc in self.index.documents.items():
            cat = doc.category.strip()
            categories.add(cat)

            # 1. Clean Title Phrasing
            clean_title = re.sub(r'[\-\–\—\(\)\[\]\,]', ' ', doc.title)
            tokens = [t.strip().lower() for t in clean_title.split() if t.strip()]

            # Add full title
            self.phrase_dict[doc.title.strip()] += 5

            # Add n-grams from title (lengths 1, 2, 3, 4)
            for length in range(1, 5):
                for i in range(len(tokens) - length + 1):
                    ngram = " ".join(tokens[i:i + length])
                    if len(ngram) >= 3 and not ngram.isdigit():
                        self.phrase_dict[ngram] += 2

            # 2. Extract key terms from text
            text_tokens = re.findall(r"[a-z0-9\']+", doc.text.lower())
            for t in text_tokens:
                if len(t) >= 3:
                    if t not in self.term_categories:
                        self.term_categories[t] = Counter()
                    self.term_categories[t][cat] += 1

        self.category_names = sorted(list(categories))

        # Add categories themselves with high frequency
        for cat in self.category_names:
            self.phrase_dict[cat.lower()] += 20
            self.phrase_dict[f"men's {cat.lower()}"] += 15
            self.phrase_dict[f"women's {cat.lower()}"] += 15

    def suggest(self, query: str, limit: int = 8) -> Dict[str, Any]:
        """
        Main suggestion entry point. Returns Amazon-style autocompletions,
        category-scoped suggestions, and direct product previews.
        """
        raw_q = query or ""
        q = raw_q.strip().lower()

        # 1. Empty query -> return curated popular searches & categories
        if not q:
            return {
                "query": raw_q,
                "is_empty": True,
                "suggestions": [
                    {
                        "text": item,
                        "displayText": item,
                        "display_prefix": "",
                        "display_completion": item,
                        "type": "popular"
                    }
                    for item in POPULAR_SEARCHES[:limit]
                ],
                "categories": [
                    {"name": cat, "photo": CANONICAL_CATEGORY_PHOTOS.get(cat, DEFAULT_FALLBACK_PHOTO)}
                    for cat in self.category_names[:6]
                ],
                "products": [],
                "corrected_from": None
            }

        # 2. Find matching phrases
        suggestions, corrected_from = self._find_phrases(q, limit=limit)

        # 3. Find category scopes (e.g. "cotton in T-Shirts")
        category_scopes = self._find_category_scopes(q, max_scopes=2)

        # 4. Find matching products
        products = self._find_matching_products(q, max_products=3)

        # Combine suggestions with category scopes (Amazon places category scope right below the 1st match)
        final_suggestions = []
        if category_scopes:
            if suggestions:
                final_suggestions.append(suggestions[0])
                final_suggestions.extend(category_scopes)
                final_suggestions.extend(suggestions[1:])
            else:
                final_suggestions.extend(category_scopes)
        else:
            final_suggestions.extend(suggestions)

        # Deduplicate and truncate to limit
        deduped = []
        seen = set()
        for item in final_suggestions:
            key = (item["type"], item["text"], item.get("category"))
            if key not in seen:
                seen.add(key)
                deduped.append(item)

        return {
            "query": raw_q,
            "is_empty": False,
            "suggestions": deduped[:limit],
            "categories": [],
            "products": products,
            "corrected_from": corrected_from
        }

    def _find_phrases(self, q: str, limit: int = 8) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """Finds query completions matching prefix `q`, falling back to typo correction if sparse."""
        matches = []
        seen = set()
        corrected_from = None

        def search_candidates(prefix: str):
            cands = []
            for phrase, count in self.phrase_dict.items():
                p_lower = phrase.lower()
                # Exact prefix match has highest score
                if p_lower.startswith(prefix):
                    score = 100 + count + (len(prefix) / (len(p_lower) + 1) * 20)
                    cands.append((score, p_lower, phrase))
                # Word-boundary prefix match (e.g. "t-shirt" matching "shirt")
                elif f" {prefix}" in p_lower:
                    score = 50 + count
                    cands.append((score, p_lower, phrase))
            cands.sort(key=lambda x: -x[0])
            return cands

        candidates = search_candidates(q)

        # Typo correction fallback if very few matches
        if len(candidates) < 2 and self.spelling_service:
            spell_info = self.spelling_service.correct_query(q)
            if spell_info.get("was_corrected"):
                corrected_q = spell_info["corrected_query"].lower()
                corrected_cands = search_candidates(corrected_q)
                if corrected_cands:
                    candidates = corrected_cands
                    corrected_from = q
                    q = corrected_q

        for score, p_lower, orig_phrase in candidates:
            if p_lower in seen:
                continue
            seen.add(p_lower)

            # Split for Amazon-style highlight: typed prefix vs bold completion
            if p_lower.startswith(q):
                display_prefix = orig_phrase[:len(q)]
                display_completion = orig_phrase[len(q):]
            else:
                display_prefix = orig_phrase
                display_completion = ""

            matches.append({
                "text": orig_phrase,
                "displayText": orig_phrase,
                "display_prefix": display_prefix,
                "display_completion": display_completion,
                "type": "query"
            })
            if len(matches) >= limit + 2:
                break

        return matches[:limit], corrected_from

    def _find_category_scopes(self, q: str, max_scopes: int = 2) -> List[Dict[str, Any]]:
        """Identifies relevant categories for the query to provide 'query in Category' suggestions."""
        scopes = []
        q_tokens = [t for t in q.split() if len(t) >= 2]
        if not q_tokens:
            return scopes

        # Map partial tokens to matching vocabulary terms in term_categories
        expanded_terms = set()
        for t in q_tokens:
            if t in self.term_categories:
                expanded_terms.add(t)
            for term in self.term_categories:
                if term.startswith(t):
                    expanded_terms.add(term)
                    if len(expanded_terms) >= 15:
                        break

        cat_counts = Counter()
        for t in expanded_terms:
            cat_counts.update(self.term_categories[t])

        for cat in self.category_names:
            if q in cat.lower():
                cat_counts[cat] += 50

        # Resolve best base word (e.g. "cot" -> "cotton")
        base_word = q
        for t in sorted(expanded_terms, key=len, reverse=True):
            if t.startswith(q) and len(t) > len(q):
                base_word = t
                break

        for cat, _ in cat_counts.most_common(max_scopes + 2):
            if q.strip() == cat.lower():
                continue
            cat_label = f"{cat}s" if not cat.endswith(('s', 'Jeans', 'Leggings', 'Dress')) else cat
            display_text = f"{base_word} in {cat_label}"
            
            # Format completion highlight
            if display_text.lower().startswith(q):
                display_prefix = display_text[:len(q)]
                display_completion = display_text[len(q):]
            else:
                display_prefix = q
                display_completion = f" in {cat_label}"

            scopes.append({
                "text": f"{base_word} {cat}",
                "category": cat,
                "displayText": display_text,
                "display_prefix": display_prefix,
                "display_completion": display_completion,
                "type": "category_scope"
            })
            if len(scopes) >= max_scopes:
                break

        return scopes

    def _find_matching_products(self, q: str, max_products: int = 3) -> List[Dict[str, Any]]:
        """Finds direct matching products in corpus for visual preview cards."""
        products = []
        tokens = [t for t in q.split() if len(t) >= 2]
        if not tokens:
            return products

        scored_docs = []
        for doc_id, doc in self.index.documents.items():
            title_lower = doc.title.lower()
            score = 0
            if q in title_lower:
                score += 10
            for t in tokens:
                if t in title_lower:
                    score += 3
                elif t in doc.category.lower():
                    score += 2

            if score > 0:
                scored_docs.append((score, doc))

        scored_docs.sort(key=lambda x: -x[0])

        for score, doc in scored_docs[:max_products]:
            products.append({
                "doc_id": doc.doc_id,
                "title": doc.title,
                "category": doc.category,
                "image_url": CANONICAL_CATEGORY_PHOTOS.get(doc.category, DEFAULT_FALLBACK_PHOTO)
            })

        return products
