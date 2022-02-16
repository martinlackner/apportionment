"""
Unit tests
"""

import pytest
import apportionment.methods as app


@pytest.mark.parametrize(
    "method",
    [
        "quota",
        "lrm",
        "hamilton",
        "largest_remainder",
        "dhondt",
        "jefferson",
        "saintelague",
        "webster",
        "huntington",
        "hill",
        "adams",
        "dean",
        "smallestdivisor",
        "harmonicmean",
        "equalproportions",
        "majorfractions",
        "greatestdivisors",
        "modified_saintelague",
    ],
)
@pytest.mark.parametrize("fractions", [True, False])
def test_all_implemented(method, fractions):
    votes = [1]
    seats = 1
    assert app.compute(method, votes, seats, fractions=fractions, verbose=False) == [1]


@pytest.mark.parametrize("method", app.METHODS)
@pytest.mark.parametrize("fractions", [True, False])
def test_weak_proportionality(method, fractions):
    votes = [14, 28, 7, 35]
    seats = 12
    assert app.compute(method, votes, seats, fractions=fractions, verbose=False) == [2, 4, 1, 5]


@pytest.mark.parametrize("method", app.METHODS)
@pytest.mark.parametrize("fractions", [True, False])
def test_zero_parties(method, fractions):
    votes = [0, 14, 28, 0, 0]
    seats = 6
    assert app.compute(method, votes, seats, fractions=fractions, verbose=False) == [0, 2, 4, 0, 0]


@pytest.mark.parametrize("method", app.METHODS)
@pytest.mark.parametrize("fractions", [True, False])
def test_fewerseatsthanparties(method, fractions):
    votes = [10, 9, 8, 8, 11, 12]
    seats = 3
    assert app.compute(method, votes, seats, fractions=fractions, verbose=False) == [1, 0, 0, 0, 1, 1]


# examples taken from
# Balinski, M. L., & Young, H. P. (1975).
# The quota method of apportionment.
# The American Mathematical Monthly, 82(7), 701-730.
@pytest.mark.parametrize(
    "method, expected",
    [
        ("quota", [52, 44, 2, 1, 1]),
        ("largest_remainder", [51, 44, 2, 2, 1]),
        ("dhondt", [52, 45, 1, 1, 1]),
        ("saintelague", [51, 43, 2, 2, 2]),
        ("modified_saintelague", [51, 43, 2, 2, 2]),
        ("huntington", [51, 43, 2, 2, 2]),
        ("adams", [51, 43, 2, 2, 2]),
        ("dean", [51, 43, 2, 2, 2]),
    ],
)
@pytest.mark.parametrize("fractions", [True, False])
def test_balinski_young_example1(method, expected, fractions):
    votes = [5117, 4400, 162, 161, 160]
    seats = 100
    assert app.compute(method, votes, seats, fractions=fractions, verbose=False) == expected


@pytest.mark.parametrize(
    "method, expected",
    [
        ("quota", [10, 7, 5, 3, 1]),
        ("largest_remainder", [9, 7, 5, 4, 1]),
        ("dhondt", [10, 7, 5, 3, 1]),
        ("saintelague", [9, 8, 5, 3, 1]),
        ("modified_saintelague", [9, 8, 5, 3, 1]),
        ("huntington", [9, 7, 6, 3, 1]),
        ("adams", [9, 7, 5, 3, 2]),
        ("dean", [9, 7, 5, 4, 1]),
    ],
)
@pytest.mark.parametrize("fractions", [True, False])
def test_balinski_young_example2(method, expected, fractions):
    votes = [9061, 7179, 5259, 3319, 1182]
    seats = 26
    assert app.compute(method, votes, seats, fractions=fractions, verbose=False) == expected


@pytest.mark.parametrize("method", app.METHODS)
@pytest.mark.parametrize("fractions", [True, False])
def test_tiebreaking(method, fractions):
    votes = [2, 1, 1, 2, 2]
    seats = 2
    assert app.compute(method, votes, seats, fractions=fractions, verbose=False) == [1, 0, 0, 1, 0]


def test_within_quota():
    votes = [5117, 4400, 162, 161, 160]
    representatives = [51, 44, 2, 2, 1]
    assert app.within_quota(votes, representatives, verbose=False)
    representatives = [52, 45, 1, 1, 1]
    assert not app.within_quota(votes, representatives, verbose=False)
    representatives = [52, 43, 2, 1, 2]
    assert not app.within_quota(votes, representatives, verbose=False)


@pytest.mark.parametrize("fractions", [True, False])
def test_threshold(fractions):
    votes = [41, 56, 3]
    seats = 60
    threshold = 0.03
    filtered_votes = app.apply_threshold(votes, threshold)
    assert filtered_votes == [41, 56, 3]
    threshold = 0.031
    filtered_votes = app.apply_threshold(votes, threshold)
    assert filtered_votes == [41, 56, 0]

    method = "dhondt"
    threshold = 0
    unfiltered_result = app.compute(
        method, votes, seats, fractions=fractions, threshold=threshold, verbose=False
    )
    threshold = 0.04
    filtered_result = app.compute(
        method, votes, seats, fractions=fractions, threshold=threshold, verbose=False
    )
    assert unfiltered_result != filtered_result


@pytest.mark.parametrize("fractions", [True, False])
def test_saintelague_difference(fractions):
    votes = [6, 1]
    seats = 4
    r1 = app.compute(
        "saintelague", votes, seats, fractions=fractions, verbose=False
    )  # [3, 1]
    r2 = app.compute(
        "modified_saintelague", votes, seats, fractions=fractions, verbose=False
    )  # [4, 0]
    assert r1 != r2


@pytest.mark.parametrize("method", app.METHODS)
@pytest.mark.parametrize("fractions", [True, False])
def test_no_ties_allowed(method, fractions):
    votes = [11, 11, 11]
    seats = 4
    if method == "quota":
        return
    with pytest.raises(app.TiesException):
        app.compute(
            method, votes, seats, fractions=fractions, tiesallowed=False, verbose=False
        )


@pytest.mark.parametrize("method", app.METHODS)
@pytest.mark.parametrize("fractions", [True, False])
def test_no_ties_allowed2(method, fractions):
    votes = [12, 12, 11, 12]
    seats = 3
    if method == "quota":
        return
    assert app.compute(
        method, votes, seats, fractions=fractions, tiesallowed=False, verbose=False
    ) == [1, 1, 0, 1]
