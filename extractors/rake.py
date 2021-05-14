import pandas as pd
from spacy.lang.en import English


class Rake:
    """."""

    def __init__(self):
        nlp = English()
        delimiters = list(nlp.Defaults.stop_words)
        delimiters.extend([",", ":", ".", "?", "!", "\n"])
        config = {"punct_chars": delimiters}
        nlp.add_pipe("sentencizer", config=config)

        self._nlp = nlp

    def extract_keywords(self, text):
        doc = self._nlp(text.lower())

        # Build co-occurrence matrix for pairs of tokens and list of candidate keywords
        candidates = []
        unique_tokens = set()
        scored_candidates = {}
        for sent in doc.sents:
            candidate_tokens = [t.text for t in self._nlp(sent.text) if
                                not t.is_stop and not t.is_punct and not t.is_space]
            candidates.append(candidate_tokens)
            unique_tokens.update(candidate_tokens)
            scored_candidates[tuple(candidate_tokens)] = 0

        cooccurrences = pd.DataFrame(0, columns=list(unique_tokens), index=list(unique_tokens))
        for candidate in candidates:
            for t1 in candidate:
                for t2 in candidate:
                    cooccurrences[t1][t2] += 1

        # Compute individual token scores
        unique_tokens = dict.fromkeys(unique_tokens)
        for key in unique_tokens:
            freq = cooccurrences[key][key]
            deg = cooccurrences[key].sum()
            unique_tokens[key] = deg / freq

        # Compute candidate keyword scores
        for candidate in scored_candidates:
            score = 0
            for t in candidate:
                score += unique_tokens[t]

            scored_candidates[candidate] = score

        # Sort in descending order
        sorted_keys = sorted(scored_candidates, key=scored_candidates.get, reverse=True)
        sorted_candidates = []
        for k in sorted_keys:
            sorted_candidates.append((" ".join(k), round(scored_candidates[k], 2)))

        return sorted_candidates
