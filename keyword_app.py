import streamlit as st
import pandas as pd
from keybert import KeyBERT


default_doc = "Machine learning is the study of computer algorithms that improve automatically through " \
              "experience and by the use of data. It is seen as a part of artificial intelligence. Machine learning " \
              "algorithms build a model based on sample data, known as \"training data\", in order to make " \
              "predictions or decisions without being explicitly programmed to do so. Machine learning algorithms " \
              "are used in a wide variety of applications, such as in medicine, email filtering, and computer vision, " \
              "where it is difficult or unfeasible to develop conventional algorithms to perform the needed tasks. A " \
              "subset of machine learning is closely related to computational statistics, which focuses on making " \
              "predictions using computers; but not all machine learning is statistical learning. The study of " \
              "mathematical optimization delivers methods, theory and application domains to the field of machine " \
              "learning. Data mining is a related field of study, focusing on exploratory data analysis through " \
              "unsupervised learning. In its application across business problems, machine learning is also " \
              "referred to as predictive analytics. "
model = KeyBERT('distilbert-base-nli-mean-tokens')


st.title('Automatic Keyword Extraction with BERT')
st.markdown("This app uses [KeyBERT](https://github.com/MaartenGr/KeyBERT) to automatically score keywords and "
            "keyphrases from text.")
st.markdown("The 'N-gram length' parameter sets the maximum length (in number of tokens) of the keyphrase. The "
            "'Diversity Algorithm' parameter sets the algorithm to determine keywords by finding a trade-off between "
            "relevancy (we want relevant keywords) and redundancy (but we do not want **too** many repeated keywords).")

st.sidebar.header("Set Parameter Values")
max_ngram_length = st.sidebar.number_input(label="N-gram Length", min_value=1, max_value=3, value=1, )
current_input = st.text_area(label="Input text:", value=default_doc, height=250)

diversity_algo = st.sidebar.radio(label="Diversity Algorithm", options=['None', 'MMR', 'MaxSum'])
use_maxsum = False
use_mmr = False
if diversity_algo == "MMR":
    use_mmr = True
elif diversity_algo == "MaxSum":
    use_maxsum = True

keywords = model.extract_keywords(current_input, keyphrase_ngram_range=(1, max_ngram_length), top_n=10,
                                  use_maxsum=use_maxsum, use_mmr=use_mmr)

df_keywords = pd.DataFrame(keywords, columns=['Keyword', 'Score'])

st.subheader("Top 10 Keywords")
st.dataframe(df_keywords, )
