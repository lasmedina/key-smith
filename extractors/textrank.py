"""TextRank class."""
from typing import List, Dict, Tuple

import networkx as nx
import spacy


class TextRank:
    """TextRank implementation for automatic keyword extraction."""

    def __init__(self):
        """Set language model and UD tags mapping."""
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = None
        self.G = nx.Graph()
        self.ud_pos_tags = {
            "Adjective": "ADJ",
            "Adposition": "ADP",
            "Adverb": "ADV",
            "Auxiliary": "AUX",
            "Coord. Conjunction": "CCONJ",
            "Determiner": "DET",
            "Interjection": "INTJ",
            "Noun": "NOUN",
            "Numeral": "NUM",
            "Particle": "PART",
            "Pronoun": "PRON",
            "Proper Noun": "PROPN",
            "Punctuation": "PUNCT",
            "Sub. Conjunction": "SCONJ",
            "Symbol": "SYM",
            "Verb": "VERB",
            "Other": "X",
        }

    def __find_cooccurrences(self, pos_tags: List[str], window_n: int) -> None:
        """Find token cooccurrences within a sliding window of n tokens.

        Selects tokens based on the part-of-speech tags. Creates unweighted, undirected graph using selected tokens
        as nodes. Creates edges between tokens if these cooccur in the text within a distance of window_n tokens from
        each other.

        Parameters
        ----------
        pos_tags: List[str]
            Full name part-of-speech tags.
        window_n: int
            Length of sliding cooccurrence window.

        Returns
        -------
        None
        """
        list_tokens = list(self.doc)
        for i in range(0, len(list_tokens) - window_n):
            token_i = list_tokens[i]
            for j in range(i, i + window_n):
                token_j = list_tokens[j]
                if token_i.pos_ in pos_tags and token_j.pos_ in pos_tags:
                    self.G.add_edge(token_i.text, token_j.text)

    def __build_keywords(self) -> Dict[Tuple[str, ...], int]:
        """Use PageRank to score candidate keywords.

        Computes a score for each token. Appends neighboring tokens to build longer keywords.

        Returns
        -------
        Dict[Tuple[str, ...], int]
            Dictionary with string lists as keys and scores as values.
        """
        list_tokens = list(self.doc)

        scored_candidates = nx.pagerank(self.G, alpha=0.85, tol=1e-4, max_iter=30)
        sorted_keys = sorted(scored_candidates, key=scored_candidates.get, reverse=True)
        sorted_candidates = {}

        for k in sorted_keys:
            sorted_candidates[k] = scored_candidates[k]

        keyphrases = {}
        keyphrase = []
        summed_scores = 0
        for i in range(len(list_tokens)):
            token_i = list_tokens[i]
            if token_i.text in sorted_keys:
                keyphrase.append(token_i.text)
                summed_scores += sorted_candidates[token_i.text]
            else:
                if len(keyphrase) > 0:
                    keyphrases[tuple(keyphrase)] = summed_scores
                keyphrase = []
                summed_scores = 0

        return keyphrases

    def extract_keywords(
        self, text: str, full_pos=None, cooccurrence_window_length=3
    ) -> List[Tuple[str, int]]:
        """Identify and score keywords in the text.

        Parameters
        ----------
        text: str
            Input text.
        full_pos: List[str]
            List of fullname part-of-speech tags.
        cooccurrence_window_length: int
            Length of sliding window, in tokens, in which to find cooccurrences.

        Returns
        -------
        List[Tuple[str, int]]
            List of (keyword, score) tuples sorted by score.
        """
        if full_pos is None:
            full_pos = ["Adjective", "Noun"]
        pos_tags = [self.ud_pos_tags[p] for p in full_pos]

        self.doc = self.nlp(text.lower())
        self.__find_cooccurrences(pos_tags, cooccurrence_window_length)
        keyphrases = self.__build_keywords()

        sorted_keyphrases = sorted(keyphrases, key=keyphrases.get, reverse=True)
        top_keyphrases = []
        for i in range(len(sorted_keyphrases)):
            top_keyphrases.append(
                (
                    " ".join(sorted_keyphrases[i]),
                    round(keyphrases[sorted_keyphrases[i]], 3),
                )
            )

        return top_keyphrases
