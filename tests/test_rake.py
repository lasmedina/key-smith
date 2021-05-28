import unittest

from extractors.rake import Rake


class RakeTestCase(unittest.TestCase):
    def test_example_from_paper(self):
        text = (
            "Compatibility of systems of linear constraints over the set of natural numbers\nCriteria of "
            "compatibility "
            "of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are "
            "considered. Upper "
            "bounds for components of a minimal set of solutions and algorithms of construction of minimal "
            "generating sets "
            "of solutions for all types of systems are given. These criteria and the corresponding algorithms for "
            "constructing a minimal supporting set of solutions can be used in solving all the considered types of "
            "systems "
            "and systems of mixed types."
        )

        rake = Rake()
        actual_keywords = rake.extract_keywords(text)
        expected_keywords = [
            ("minimal generating sets", 8.67),
            ("linear diophantine equations", 8.5),
            ("minimal supporting set", 7.67),
            ("minimal set", 4.67),
            ("linear constraints", 4.5),
            ("natural numbers", 4.0),
            ("strict inequations", 4.0),
            ("nonstrict inequations", 4.0),
            ("upper bounds", 4.0),
            ("mixed types", 3.67),
            ("corresponding algorithms", 3.5),
            ("considered types", 3.17),
            ("set", 2.0),
            ("types", 1.67),
            ("considered", 1.5),
            ("algorithms", 1.5),
            ("compatibility", 1.0),
            ("systems", 1.0),
            ("criteria", 1.0),
            ("system", 1.0),
            ("components", 1.0),
            ("solutions", 1.0),
            ("construction", 1.0),
            ("given", 1.0),
            ("constructing", 1.0),
            ("solving", 1.0),
        ]

        self.assertListEqual(expected_keywords, actual_keywords)
