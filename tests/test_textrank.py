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

        textrank = TextRank()
        actual_keywords = textrank.extract_keywords(text)
        expected_keywords = {('linear', 'diophantine', 'equations'): 0.12909098715935866, ('minimal', 'generating', 'sets'): 0.12328705522540664, ('minimal', 'set'): 0.11282312634758349, ('linear', 'constraints'): 0.08726551819217813, ('nonstrict', 'inequations'): 0.07979547401305309, ('strict', 'inequations'): 0.0793495898728744}

        self.assertDictEqual(actual_keywords, expected_keywords)
