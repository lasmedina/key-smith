import networkx as nx
import spacy
from spacy.matcher import PhraseMatcher


class TextRank:
    """."""

    def __init__(self):
        self._nlp = spacy.load("en_core_web_sm")
        self.doc = None
        self.window_n = 10
        self.top_candidates = 6
        self.G = nx.Graph()

    def __find_cooccurrences(self):
        list_tokens = list(self.doc)
        for i in range(0, len(list_tokens) - self.window_n):
            for j in range(i, i + self.window_n):
                if list_tokens[i].pos_ in ['ADJ', 'NOUN'] and list_tokens[j].pos_ in ['ADJ', 'NOUN']:
                    self.G.add_edge(list_tokens[i].text, list_tokens[j].text)

    def __run_pagerank(self):
        scored_candidates = nx.pagerank(self.G, alpha=0.85, tol=1e-4, max_iter=30)
        sorted_keys = sorted(scored_candidates, key=scored_candidates.get, reverse=True)
        sorted_candidates = {}

        for k in sorted_keys:
            sorted_candidates[k] = scored_candidates[k]

        list_tokens = list(self.doc)
        keyphrases = {}
        keyphrase = []
        summed_scores = 0
        for i in range(len(list_tokens)):
            if list_tokens[i].text in sorted_keys:
                keyphrase.append(list_tokens[i].text)
                summed_scores += sorted_candidates[list_tokens[i].text]
            else:
                if len(keyphrase) > 0:
                    keyphrases[tuple(keyphrase)] = summed_scores
                keyphrase = []
                summed_scores = 0

        return keyphrases

    def extract_keywords(self, text):
        self.doc = self._nlp(text.lower())
        self.__find_cooccurrences()
        keyphrases = self.__run_pagerank()

        sorted_keyphrases = sorted(keyphrases, key=keyphrases.get, reverse=True)
        top_keyphrases = {}
        for i in range(self.top_candidates):
            top_keyphrases[sorted_keyphrases[i]] = keyphrases[sorted_keyphrases[i]]

        return top_keyphrases
