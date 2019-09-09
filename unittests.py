# Unit tests

# Author: Martin Lackner


import unittest
import apportionment


METHODS = ["quota", "largest_remainder", "dhondt",
           "saintelague", "huntington", "adams"]


class TestApprovalMultiwinner(unittest.TestCase):

    def test_weak_proportionality(self):
        self.longMessage = True

        distribution = [14, 28, 7, 35]
        seats = 12
        for method in METHODS:
            result = apportionment.method(method, distribution,
                                          seats, verbose=False)
            self.assertEqual(result, [2, 4, 1, 5],
                             msg=method + " failed")

    def test_zero_parties(self):
        self.longMessage = True

        distribution = [0, 14, 28, 0, 0]
        seats = 6
        for method in METHODS:
            result = apportionment.method(method, distribution,
                                          seats, verbose=False)
            self.assertEqual(result, [0, 2, 4, 0, 0],
                             msg=method + " failed")

    def test_fewerseatsthanparties(self):
        self.longMessage = True

        distribution = [10, 9, 8, 8, 11, 12]
        seats = 3
        for method in METHODS:
            result = apportionment.method(method, distribution,
                                          seats, verbose=False)
            self.assertEqual(result, [1, 0, 0, 0, 1, 1],
                             msg=method + " failed")

if __name__ == '__main__':
    unittest.main()
