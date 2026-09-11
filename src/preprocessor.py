"""
Information Retrieval Preprocessor Module (CSD358)
==================================================
Handles document and query text preprocessing:
1. Tokenization (alphanumeric extraction, punctuation removal)
2. Case Normalization (lowercasing)
3. Stop-Word Removal (consistent English stop-word policy)
4. Stemming (Porter Stemming Algorithm)

Stop-Word Policy Justification:
--------------------------------
In accordance with Part A requirements:
Stop words are high-frequency grammatical functional words (articles, prepositions,
conjunctions, auxiliary verbs such as 'the', 'is', 'at', 'which', 'on', 'and', 'for')
that appear abundantly across clothing descriptions without providing semantic
differentiation between garment types, fits, fabrics, or attributes.
Removing them reduces inverted index size, lowers computational overhead in VSM cosine
similarity calculations, and avoids skewing document length normalization.
Crucially, the exact same stop-word list and tokenization pipeline is applied
consistently across document indexing, free-text query parsing, and positional queries.
"""

import re
from typing import List, Tuple, Set


class PorterStemmer:
    """
    Standard implementation of Martin Porter's 1980 stemming algorithm.
    Provides rule-based suffix stripping for English vocabulary.
    """

    def __init__(self):
        self.b = ""
        self.k = 0
        self.k0 = 0
        self.j = 0

    def _is_consonant(self, i: int) -> bool:
        c = self.b[i]
        if c in ('a', 'e', 'i', 'o', 'u'):
            return False
        if c == 'y':
            if i == self.k0:
                return True
            else:
                return not self._is_consonant(i - 1)
        return True

    def _measure(self) -> int:
        n = 0
        i = self.k0
        while True:
            if i > self.j:
                return n
            if not self._is_consonant(i):
                break
            i += 1
        i += 1
        while True:
            while True:
                if i > self.j:
                    return n
                if self._is_consonant(i):
                    break
                i += 1
            i += 1
            n += 1
            while True:
                if i > self.j:
                    return n
                if not self._is_consonant(i):
                    break
                i += 1
            i += 1

    def _vowel_in_stem(self) -> bool:
        for i in range(self.k0, self.j + 1):
            if not self._is_consonant(i):
                return True
        return False

    def _double_consonant(self, i: int) -> bool:
        if i < self.k0 + 1:
            return False
        if self.b[i] != self.b[i - 1]:
            return False
        return self._is_consonant(i)

    def _cvc(self, i: int) -> bool:
        if i < self.k0 + 2 or not self._is_consonant(i) or self._is_consonant(i - 1) or not self._is_consonant(i - 2):
            return False
        ch = self.b[i]
        if ch in ('w', 'x', 'y'):
            return False
        return True

    def _ends(self, s: str) -> bool:
        length = len(s)
        o = self.k - length + 1
        if o < self.k0:
            return False
        for i in range(length):
            if self.b[o + i] != s[i]:
                return False
        self.j = self.k - length
        return True

    def _set_to(self, s: str):
        length = len(s)
        o = self.j + 1
        self.b = self.b[:o] + s + self.b[o + length:]
        self.k = self.j + length

    def _replace(self, s: str):
        if self._measure() > 0:
            self._set_to(s)

    def _step1ab(self):
        if self.b[self.k] == 's':
            if self._ends("sses"):
                self.k -= 2
            elif self._ends("ies"):
                self._set_to("i")
            elif self.b[self.k - 1] != 's':
                self.k -= 1
        if self._ends("eed"):
            if self._measure() > 0:
                self.k -= 1
        elif (self._ends("ed") or self._ends("ing")) and self._vowel_in_stem():
            self.k = self.j
            if self._ends("at"):
                self._set_to("ate")
            elif self._ends("bl"):
                self._set_to("ble")
            elif self._ends("iz"):
                self._set_to("ize")
            elif self._double_consonant(self.k):
                self.k -= 1
                ch = self.b[self.k]
                if ch in ('l', 's', 'z'):
                    self.k += 1
            elif self._measure() == 1 and self._cvc(self.k):
                self._set_to("e")

    def _step1c(self):
        if self._ends("y") and self._vowel_in_stem():
            self.b = self.b[:self.k] + 'i' + self.b[self.k + 1:]

    def _step2(self):
        if self.k <= self.k0:
            return
        c = self.b[self.k - 1]
        if c == 'a':
            if self._ends("ational"): self._replace("ate")
            elif self._ends("tional"): self._replace("tion")
        elif c == 'c':
            if self._ends("enci"): self._replace("ence")
            elif self._ends("anci"): self._replace("ance")
        elif c == 'e':
            if self._ends("izer"): self._replace("ize")
        elif c == 'l':
            if self._ends("bli"): self._replace("ble")
            elif self._ends("alli"): self._replace("al")
            elif self._ends("entli"): self._replace("ent")
            elif self._ends("eli"): self._replace("e")
            elif self._ends("ousli"): self._replace("ous")
        elif c == 'o':
            if self._ends("ization"): self._replace("ize")
            elif self._ends("ation"): self._replace("ate")
            elif self._ends("ator"): self._replace("ate")
        elif c == 's':
            if self._ends("alism"): self._replace("al")
            elif self._ends("iveness"): self._replace("ive")
            elif self._ends("fulness"): self._replace("ful")
            elif self._ends("ousness"): self._replace("ous")
        elif c == 't':
            if self._ends("aliti"): self._replace("al")
            elif self._ends("iviti"): self._replace("ive")
            elif self._ends("biliti"): self._replace("ble")
        elif c == 'g':
            if self._ends("logi"): self._replace("log")

    def _step3(self):
        if self.k <= self.k0:
            return
        c = self.b[self.k]
        if c == 'e':
            if self._ends("icate"): self._replace("ic")
            elif self._ends("ative"): self._replace("")
            elif self._ends("alize"): self._replace("al")
        elif c == 'i':
            if self._ends("iciti"): self._replace("ic")
        elif c == 'l':
            if self._ends("ical"): self._replace("ic")
            elif self._ends("ful"): self._replace("")
        elif c == 's':
            if self._ends("ness"): self._replace("")

    def _step4(self):
        if self.k <= self.k0:
            return
        c = self.b[self.k - 1]
        if c == 'a':
            if self._ends("al"):
                if self._measure() > 1: self.k = self.j
        elif c == 'c':
            if self._ends("ance") or self._ends("ence"):
                if self._measure() > 1: self.k = self.j
        elif c == 'e':
            if self._ends("er"):
                if self._measure() > 1: self.k = self.j
        elif c == 'i':
            if self._ends("ic"):
                if self._measure() > 1: self.k = self.j
        elif c == 'l':
            if self._ends("able") or self._ends("ible"):
                if self._measure() > 1: self.k = self.j
        elif c == 'n':
            if self._ends("ant") or self._ends("ement") or self._ends("ment") or self._ends("ent"):
                if self._measure() > 1: self.k = self.j
        elif c == 'o':
            if self._ends("ion") and self.j >= self.k0 and self.b[self.j] in ('s', 't'):
                if self._measure() > 1: self.k = self.j
            elif self._ends("ou"):
                if self._measure() > 1: self.k = self.j
        elif c == 's':
            if self._ends("ism"):
                if self._measure() > 1: self.k = self.j
        elif c == 't':
            if self._ends("ate") or self._ends("iti"):
                if self._measure() > 1: self.k = self.j
        elif c == 'u':
            if self._ends("ous"):
                if self._measure() > 1: self.k = self.j
        elif c == 'v':
            if self._ends("ive"):
                if self._measure() > 1: self.k = self.j
        elif c == 'z':
            if self._ends("ize"):
                if self._measure() > 1: self.k = self.j

    def _step5(self):
        self.j = self.k
        if self.b[self.k] == 'e':
            a = self._measure()
            if a > 1 or (a == 1 and not self._cvc(self.k - 1)):
                self.k -= 1
        if self.b[self.k] == 'l' and self._double_consonant(self.k) and self._measure() > 1:
            self.k -= 1

    def stem(self, word: str) -> str:
        word = word.lower()
        if len(word) <= 2:
            return word
        self.b = word
        self.k = len(word) - 1
        self.k0 = 0
        self._step1ab()
        self._step1c()
        self._step2()
        self._step3()
        self._step4()
        self._step5()
        return self.b[:self.k + 1]


# Standard English Stop Words (consistently applied across corpus & queries)
STOP_WORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}


class Preprocessor:
    """
    Standard preprocessor for clothing corpus & search queries.
    """

    def __init__(self, stop_words: Set[str] = None):
        self.stemmer = PorterStemmer()
        self.stop_words = stop_words if stop_words is not None else STOP_WORDS

    def tokenize_raw(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Tokenizes text while tracking start and end character offsets.
        Returns list of (token_str, start_char_idx, end_char_idx).
        Punctuation is removed by extracting alphanumeric tokens.
        """
        tokens = []
        for match in re.finditer(r'[A-Za-z0-9]+', text):
            tokens.append((match.group(0), match.start(), match.end()))
        return tokens

    def preprocess_tokens_with_positions(self, text: str) -> List[Tuple[str, int, int, int]]:
        """
        Executes full preprocessing:
        1. Tokenize & normalize case (lowercase)
        2. Filter out stop-words
        3. Porter stemming
        Returns list of tuples: (stemmed_term, token_position, start_char, end_char)
        where token_position is the sequence index (0, 1, 2, ...) of the retained term.
        """
        raw_tokens = self.tokenize_raw(text)
        processed = []
        pos = 0
        for raw_tok, start_idx, end_idx in raw_tokens:
            token_lower = raw_tok.lower()
            if token_lower in self.stop_words:
                continue
            stemmed = self.stemmer.stem(token_lower)
            processed.append((stemmed, pos, start_idx, end_idx))
            pos += 1
        return processed

    def preprocess(self, text: str) -> List[str]:
        """
        Returns simple list of stemmed terms (without positional indices).
        """
        tokens_with_pos = self.preprocess_tokens_with_positions(text)
        return [t[0] for t in tokens_with_pos]

    def stem_word(self, word: str) -> str:
        """Helper to stem a single word."""
        return self.stemmer.stem(word.lower())
