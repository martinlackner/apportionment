# Unit tests

# Author: Martin Lackner


import unittest
import apportionment.methods as app


METHODS = ["quota", "largest_remainder", "dhondt", "saintelague",
           "modified_saintelague", "huntington", "adams", "dean"]


class TestApprovalMultiwinner(unittest.TestCase):

    def test_all_implemented(self):
        ALLMETHODSSTRINGS = ["quota", "lrm", "hamilton", "largest_remainder",
                             "dhondt", "jefferson", "saintelague", "webster",
                             "huntington", "hill", "adams", "dean",
                             "smallestdivisor", "harmonicmean",
                             "equalproportions", "majorfractions",
                             "greatestdivisors", "modified_saintelague"]

        votes = [1]
        seats = 1
        for method in ALLMETHODSSTRINGS:
            result = app.compute(method, votes,
                                 seats, verbose=False)
            self.assertEqual(result, [1],
                             msg=method + " does not exist")

    def test_weak_proportionality(self):
        self.longMessage = True

        votes = [14, 28, 7, 35]
        seats = 12
        for method in METHODS:
            result = app.compute(method, votes,
                                 seats, verbose=False)
            self.assertEqual(result, [2, 4, 1, 5],
                             msg=method + " failed")

    def test_zero_parties(self):
        self.longMessage = True

        votes = [0, 14, 28, 0, 0]
        seats = 6
        for method in METHODS:
            result = app.compute(method, votes,
                                 seats, verbose=False)
            self.assertEqual(result, [0, 2, 4, 0, 0],
                             msg=method + " failed")

    def test_fewerseatsthanparties(self):
        self.longMessage = True

        votes = [10, 9, 8, 8, 11, 12]
        seats = 3
        for method in METHODS:
            result = app.compute(method, votes,
                                 seats, verbose=False)
            self.assertEqual(result, [1, 0, 0, 0, 1, 1],
                             msg=method + " failed")

    # example taken from
    # Balinski, M. L., & Young, H. P. (1975).
    # The quota method of apportionment.
    # The American Mathematical Monthly, 82(7), 701-730.
    def test_balinski_young_example1(self):
        self.longMessage = True

        RESULTS = {"quota": [52, 44, 2, 1, 1],
                   "largest_remainder": [51, 44, 2, 2, 1],
                   "dhondt": [52, 45, 1, 1, 1],
                   "saintelague": [51, 43, 2, 2, 2],
                   "modified_saintelague": [51, 43, 2, 2, 2],
                   "huntington": [51, 43, 2, 2, 2],
                   "adams": [51, 43, 2, 2, 2],
                   "dean": [51, 43, 2, 2, 2]
                   }

        votes = [5117, 4400, 162, 161, 160]
        seats = 100
        for method in RESULTS.keys():
            result = app.compute(method, votes,
                                 seats, verbose=False)
            self.assertEqual(result, RESULTS[method],
                             msg=method + " failed")

    def test_balinski_young_example2(self):
        self.longMessage = True

        RESULTS = {"quota": [10, 7, 5, 3, 1],
                   "largest_remainder": [9, 7, 5, 4, 1],
                   "dhondt": [10, 7, 5, 3, 1],
                   "saintelague": [9, 8, 5, 3, 1],
                   "modified_saintelague": [9, 8, 5, 3, 1],
                   "huntington": [9, 7, 6, 3, 1],
                   "adams": [9, 7, 5, 3, 2],
                   "dean": [9, 7, 5, 4, 1]
                   }

        votes = [9061, 7179, 5259, 3319, 1182]
        seats = 26
        for method in RESULTS.keys():
            result = app.compute(method, votes,
                                 seats, verbose=False)
            self.assertEqual(result, RESULTS[method],
                             msg=method + " failed")

    def test_tiebreaking(self):
        self.longMessage = True

        votes = [2, 1, 1, 2, 2]
        seats = 2
        for method in METHODS:
            result = app.compute(method, votes,
                                 seats, verbose=False)
            self.assertEqual(result, [1, 0, 0, 1, 0],
                             msg=method + " failed")

    def test_within_quota(self):
        votes = [5117, 4400, 162, 161, 160]
        representatives = [51, 44, 2, 2, 1]
        self.assertTrue(app.within_quota(votes, representatives,
                                         verbose=False))
        representatives = [52, 45, 1, 1, 1]
        self.assertFalse(app.within_quota(votes, representatives,
                                          verbose=False))
        representatives = [52, 43, 2, 1, 2]
        self.assertFalse(app.within_quota(votes, representatives,
                                          verbose=False))

    def test_threshold(self):
        votes = [41, 56, 3]
        seats = 60
        threshold = 0.03
        filtered_votes = app.apply_threshold(votes, threshold)
        self.assertEqual(filtered_votes, [41, 56, 3],
                         "Threshold cut too much.")
        threshold = 0.031
        filtered_votes = app.apply_threshold(votes, threshold)
        self.assertEqual(filtered_votes, [41, 56, 0],
                         "Threshold was not applied correctly.")

        method = "dhondt"
        threshold = 0
        unfiltered_result = app.compute(method, votes, seats,
                                        threshold=threshold,
                                        verbose=False)
        threshold = 0.04
        filtered_result = app.compute(method, votes, seats,
                                      threshold=threshold,
                                      verbose=False)
        self.assertNotEqual(unfiltered_result, filtered_result,
                            "Result did not change despite threshold")

    def test_saintelague_difference(self):
        votes = [6, 1]
        seats = 4
        r1 = app.compute("saintelague", votes,
                         seats, verbose=False)  # [3, 1]
        r2 = app.compute("modified_saintelague", votes,
                         seats, verbose=False)  # [4, 0]
        self.assertNotEqual(r1, r2,
                            "Saintelague and its modified variant"
                            + "should produce differents results.")


if __name__ == '__main__':
    unittest.main()
