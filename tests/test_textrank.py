import unittest

from extractors.textrank import TextRank


class TextRankTestCase(unittest.TestCase):

    def test_example_from_paper(self):
        text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of " \
               "compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict " \
               "inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms " \
               "of construction of minimal generating sets of solutions for all types of systems are given. These " \
               "criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can " \
               "be used in solving all the considered types of systems and systems of mixed types."

        # Paper does not specify parameter values (e.g. window length), thus this is an approximation with chosen
        # default cooccurrence window length of 3 and top candidates of 10.
        textrank = TextRank()
        actual_keywords = textrank.extract_keywords(text)
        expected_keywords = [('linear diophantine equations', 0.156),
                             ('minimal generating sets', 0.129),
                             ('linear constraints', 0.1),
                             ('minimal set', 0.096),
                             ('upper bounds', 0.085),
                             ('strict inequations', 0.082),
                             ('natural numbers', 0.075),
                             ('nonstrict inequations', 0.075),
                             ('systems', 0.066),
                             ('minimal', 0.053)
                             ]

        self.assertListEqual(actual_keywords, expected_keywords)

    def test_pos_tag_mapping(self):
        full_pos = ['Noun', 'Adjective', 'Verb', 'Other']
        exp_ud_pos_tags = ['NOUN', 'ADJ', 'VERB', 'X']

        extractor = TextRank()
        act_us_pos_tags = extractor._TextRank__map_pos_tags(full_pos)

        self.assertListEqual(act_us_pos_tags, exp_ud_pos_tags)

