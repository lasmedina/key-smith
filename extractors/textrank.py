import networkx as nx
import spacy


class TextRank:
    """TextRank for automatic keyword extraction."""

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = None
        self.G = nx.Graph()
        self.ud_pos_tags = {'Adjective': 'ADJ', 'Adposition': 'ADP', 'Adverb': 'ADV', 'Auxiliary': 'AUX',
                            'Coord. Conjunction': 'CCONJ', 'Determiner': 'DET', 'Interjection': 'INTJ', 'Noun': 'NOUN',
                            'Numeral': 'NUM', 'Particle': 'PART', 'Pronoun': 'PRON', 'Proper Noun': 'PROPN',
                            'Punctuation': 'PUNCT', 'Sub. Conjunction': 'SCONJ', 'Symbol': 'SYM', 'Verb': 'VERB',
                            'Other': 'X'}

    def __find_cooccurrences(self, pos_tags, window_n):
        list_tokens = list(self.doc)
        for i in range(0, len(list_tokens) - window_n):
            token_i = list_tokens[i]
            for j in range(i, i + window_n):
                token_j = list_tokens[j]
                if token_i.pos_ in pos_tags and token_j.pos_ in pos_tags:
                    self.G.add_edge(token_i.text, token_j.text)

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

    def __map_pos_tags(self, full_pos):
        return [self.ud_pos_tags[p] for p in full_pos]

    def extract_keywords(self, text, full_pos=None, cooccurrence_window_length=3):
        if full_pos is None:
            full_pos = ['Adjective', 'Noun']
        pos_tags = self.__map_pos_tags(full_pos)

        self.doc = self.nlp(text.lower())
        self.__find_cooccurrences(pos_tags, cooccurrence_window_length)
        keyphrases = self.__run_pagerank()

        sorted_keyphrases = sorted(keyphrases, key=keyphrases.get, reverse=True)
        top_keyphrases = []
        for i in range(len(sorted_keyphrases)):
            top_keyphrases.append((" ".join(sorted_keyphrases[i]),
                                   round(keyphrases[sorted_keyphrases[i]], 3)))

        return top_keyphrases
