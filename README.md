# key-smith

Simple, unsupervised, keyword extraction. Includes custom implementations of:

- RAKE
- TextRank
- ...more coming soon

#### Example 1 - TextRank

```
text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of " \
    "compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict " \
    "inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms " \
    "of construction of minimal generating sets of solutions for all types of systems are given. These " \
    "criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can " \
    "be used in solving all the considered types of systems and systems of mixed types."

extractor = TextRank()
keywords = extractor.extract_keywords(text)
```

#### Example 2 - RAKE
```
extractor = Rake()
keywords = extractor.extract_keywords(text)
```

#### Example 3 - TextRank with custom arguments
```
# Set part-of-speech tags with which to select candidate keywords.
# For more info see:
extractor = TextRank()
pos_tags = ['ADJ', 'VERB', 'NOUN']

# Define the length of the cooccurrence window.
window_n = 5

keywords = extractor.extract_keywords(text, pos_tags, window_n)
```

### App

You can also use the app to easily change parameter values and test the keyword extraction methods:

`streamlit run keyword_app.py`

In addition to the keyword extraction methods in this repo, the app also makes available [KeyBERT](https://github.com/MaartenGr/KeyBERT), a keyword scoring method based on BERT.


### References

Papers

- Rose, S. et al (2010) Automatic Keyword Extraction from Individual Documents, in Text Mining: Applications and Theory. Wiley.
- Mihalcea, R. and Tarau, P. (2004) TextRank: Bringing order into texts. In Proceedings of EMNLP 2004, pp. 404–411. ACL

Repos
- [KeyBERT](https://github.com/MaartenGr/KeyBERT)