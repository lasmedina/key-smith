"""App entry point."""
import streamlit as st
import pandas as pd
from keybert import KeyBERT

from extractors.rake import Rake
from extractors.textrank import TextRank


def display_results():
    """Extract keywords from input text.

    Returns
    -------
    None
    """
    keywords = []

    if extractor_algo == "KeyBERT":
        st.markdown("[KeyBERT](https://github.com/MaartenGr/KeyBERT) input parameters:")
        st.markdown(
            "   - 'N-gram length': sets the maximum length (in number of tokens) of the keyphrase"
        )
        st.markdown(
            "   - 'Diversity Algorithm': sets the algorithm to determine keywords by finding a trade-off "
            "between relevancy (we want relevant keywords) and redundancy (but we do not want **too** many "
            "repeated keywords)."
        )
        max_ngram_length = st.sidebar.number_input(
            label="N-gram Length",
            min_value=1,
            max_value=3,
            value=1,
        )
        diversity_algo = st.sidebar.radio(
            label="Diversity Algorithm", options=["None", "MMR", "MaxSum"]
        )
        use_maxsum = False
        use_mmr = False
        if diversity_algo == "MMR":
            use_mmr = True
        elif diversity_algo == "MaxSum":
            use_maxsum = True
        keywords = model.extract_keywords(
            current_input,
            keyphrase_ngram_range=(1, max_ngram_length),
            top_n=10,
            use_maxsum=use_maxsum,
            use_mmr=use_mmr,
        )
    elif extractor_algo == "RAKE":
        st.markdown(
            "RAKE (Rapid Automatic Keyword Extraction) implementation inspired by the [original paper]("
            "https://www.researchgate.net/publication"
            "/227988510_Automatic_Keyword_Extraction_from_Individual_Documents)"
        )
        extractor = Rake()
        keywords = extractor.extract_keywords(current_input)
        keywords = keywords[:10]

    elif extractor_algo == "TextRank":
        st.markdown(
            "TextRank implementation inspired by the [original paper]("
            "https://www.aclweb.org/anthology/W04-3252.pdf)"
        )
        extractor = TextRank()
        window_length = st.sidebar.number_input(
            label="Window Length", min_value=1, max_value=10, value=1
        )
        pos_tags = st.sidebar.multiselect(
            "Part-of-speech Tags",
            [
                "Adjective",
                "Adposition",
                "Adverb",
                "Auxiliary",
                "Coord. Conjunction",
                "Determiner",
                "Interjection",
                "Noun",
                "Numeral",
                "Particle",
                "Pronoun",
                "Proper Noun",
                "Punctuation",
                "Sub. Conjunction",
                "Symbol",
                "Verb",
                "Other",
            ],
            ["Adjective", "Noun"],
        )
        keywords = extractor.extract_keywords(current_input, pos_tags, window_length)
        keywords = keywords[:10]
    return keywords


default_doc = (
    "Compatibility of systems of linear constraints over the set of natural numbers\nCriteria of "
    "compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict "
    "inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms "
    "of construction of minimal generating sets of solutions for all types of systems are given. These "
    "criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can "
    "be used in solving all the considered types of systems and systems of mixed types. "
)

model = KeyBERT("distilbert-base-nli-mean-tokens")

st.title("Automatic Keyword Extraction")

st.markdown("<br>", unsafe_allow_html=True)
"""
[![Star](https://raw.githubusercontent.com/lasmedina/key-smith/master/GitHub-Mark-Light-32px.png)](https://github.com/lasmedina/key-smith)
"""


st.markdown(" 1. Paste your text below")
st.markdown(" 2. Select an extractor algorithm")
st.markdown(" 3. Et voil??!")

current_input = st.text_area(label="Input text:", value=default_doc, height=250)
st.sidebar.header("Set Parameter Values")
extractor_algo = st.sidebar.radio(
    label="Extractor", options=["None", "KeyBERT", "RAKE", "TextRank"]
)

keywords = display_results()
df_keywords = pd.DataFrame(keywords, columns=["Keyword", "Score"])

st.subheader("Top 10 Keywords")
st.dataframe(
    df_keywords,
)
