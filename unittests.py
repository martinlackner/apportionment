# Unit tests

# Author: Martin Lackner


import unittest
import apportionment


METHODS = ["quota", "largest_remainder", "dhondt",
           "saintelague", "huntington", "adams", "dean"]


class TestApprovalMultiwinner(unittest.TestCase):

    def test_all_implemented(self):
        ALLMETHODSSTRINGS = ["quota", "lrm", "hamilton", "largest_remainder",
                             "dhondt", "jefferson", "saintelague", "webster",
                             "huntington", "hill", "adams", "dean",
                             "smallestdivisor", "harmonicmean",
                             "equalproportions", "majorfractions",
                             "greatestdivisors"]

        votes = [1]
        seats = 1
        for method in ALLMETHODSSTRINGS:
            result = apportionment.method(method, votes,
                                          seats, verbose=False)
            self.assertEqual(result, [1],
                             msg=method + " does not exist")

    def test_weak_proportionality(self):
        self.longMessage = True

        votes = [14, 28, 7, 35]
        seats = 12
        for method in METHODS:
            result = apportionment.method(method, votes,
                                          seats, verbose=False)
            self.assertEqual(result, [2, 4, 1, 5],
                             msg=method + " failed")

    def test_zero_parties(self):
        self.longMessage = True

        votes = [0, 14, 28, 0, 0]
        seats = 6
        for method in METHODS:
            result = apportionment.method(method, votes,
                                          seats, verbose=False)
            self.assertEqual(result, [0, 2, 4, 0, 0],
                             msg=method + " failed")

    def test_fewerseatsthanparties(self):
        self.longMessage = True

        votes = [10, 9, 8, 8, 11, 12]
        seats = 3
        for method in METHODS:
            result = apportionment.method(method, votes,
                                          seats, verbose=False)
            self.assertEqual(result, [1, 0, 0, 0, 1, 1],
                             msg=method + " failed")

    # example taken from
    # Balinski, M. L., & Young, H. P. (1975).
    # The quota method of apportionment.
    # The American Mathematical Monthly, 82(7), 701-730.
    def test_balinski_young_example(self):
        self.longMessage = True

        RESULTS = {"quota": [52, 44, 2, 1, 1],
                   "largest_remainder": [51, 44, 2, 2, 1],
                   "dhondt": [52, 45, 1, 1, 1],
                   "saintelague": [51, 43, 2, 2, 2],
                   "huntington": [51, 43, 2, 2, 2],
                   "adams": [51, 43, 2, 2, 2],
                   "dean": [51, 43, 2, 2, 2]
                   }

        votes = [5117, 4400, 162, 161, 160]
        seats = 100
        for method in RESULTS.keys():
            result = apportionment.method(method, votes,
                                          seats, verbose=False)
            self.assertEqual(result, RESULTS[method],
                             msg=method + " failed")

    def test_tiebreaking(self):
        self.longMessage = True

        votes = [2, 1, 1, 2, 2]
        seats = 2
        for method in METHODS:
            result = apportionment.method(method, votes,
                                          seats, verbose=False)
            self.assertEqual(result, [1, 0, 0, 1, 0],
                             msg=method + " failed")

    def test_within_quota(self):
        votes = [5117, 4400, 162, 161, 160]
        representatives = [51, 44, 2, 2, 1]
        self.assertTrue(apportionment.within_quota(votes, representatives,
                                                   verbose=False))
        representatives = [52, 45, 1, 1, 1]
        self.assertFalse(apportionment.within_quota(votes, representatives,
                                                    verbose=False))
        representatives = [52, 43, 2, 1, 2]
        self.assertFalse(apportionment.within_quota(votes, representatives,
                                                    verbose=False))


if __name__ == '__main__':
    unittest.main()
