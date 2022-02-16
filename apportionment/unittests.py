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
    assert app.compute(method, votes, seats, fractions=fractions, verbose=False) == [
        2,
        4,
        1,
        5,
    ]


@pytest.mark.parametrize("method", app.METHODS)
@pytest.mark.parametrize("fractions", [True, False])
def test_zero_parties(method, fractions):
    votes = [0, 14, 28, 0, 0]
    seats = 6
    assert app.compute(method, votes, seats, fractions=fractions, verbose=False) == [
        0,
        2,
        4,
        0,
        0,
    ]


@pytest.mark.parametrize("method", app.METHODS)
@pytest.mark.parametrize("fractions", [True, False])
def test_fewerseatsthanparties(method, fractions):
    votes = [10, 9, 8, 8, 11, 12]
    seats = 3
    assert app.compute(method, votes, seats, fractions=fractions, verbose=False) == [
        1,
        0,
        0,
        0,
        1,
        1,
    ]


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
    assert (
        app.compute(method, votes, seats, fractions=fractions, verbose=False)
        == expected
    )


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
    assert (
        app.compute(method, votes, seats, fractions=fractions, verbose=False)
        == expected
    )


@pytest.mark.parametrize("method", app.METHODS)
@pytest.mark.parametrize("fractions", [True, False])
def test_tiebreaking(method, fractions):
    votes = [2, 1, 1, 2, 2]
    seats = 2
    assert app.compute(method, votes, seats, fractions=fractions, verbose=False) == [
        1,
        0,
        0,
        1,
        0,
    ]


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


@pytest.mark.parametrize(
    "year, partynames, votes, officialresult",
    [
        (
            2019,
            [
                "ÖVP",
                "SPÖ",
                "FPÖ",
                "NEOS",
                "JETZT",
                "GRÜNE",
                "KPÖ",
                "WANDL",
                "BZÖ",
                "BIER",
                "CPÖ",
                "GILT",
                "SLP",
            ],
            [
                1789417,
                1011868,
                772666,
                387124,
                89169,
                664055,
                32736,
                22168,
                760,
                4946,
                260,
                1767,
                310,
            ],
            [71, 40, 31, 15, 0, 26, 0, 0, 0, 0, 0, 0, 0],
        ),
        (
            2017,
            [
                "SPÖ",
                "ÖVP",
                "FPÖ",
                "GRÜNE",
                "NEOS",
                "PILZ",
                "GILT",
                "FLÖ",
                "KPÖ",
                "WEIßE",
                "SLP",
                "EUAUS",
                "M",
                "CPÖ",
                "NBZ",
                "ODP",
            ],
            [
                1361746,
                1595526,
                1316442,
                192638,
                268518,
                223543,
                48234,
                8889,
                39689,
                9167,
                713,
                693,
                221,
                425,
                2724,
                761,
            ],
            [52, 62, 51, 0, 10, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ),
        (
            2013,
            [
                "SPÖ",
                "ÖVP",
                "FPÖ",
                "BZÖ",
                "GRÜNE",
                "FRANK",
                "NEOS",
                "KPÖ",
                "PIRAT",
                "CPÖ",
                "WANDL",
                "M",
                "EUAUS",
                "SLP",
            ],
            [
                1258605,
                1125876,
                962313,
                165746,
                582657,
                268679,
                232946,
                48175,
                36265,
                6647,
                3051,
                490,
                510,
                947,
            ],
            [52, 47, 40, 0, 24, 11, 9, 0, 0, 0, 0, 0, 0, 0],
        ),
        (
            2008,
            [
                "SPÖ",
                "ÖVP",
                "GRÜNE",
                "FPÖ",
                "BZÖ",
                "FRITZ",
                "DC",
                "KPÖ",
                "LIF",
                "RETTÖ",
                "LINKE",
                "KLEMENTE",
                "LINKE",
                "STARK",
                "TRP",
            ],
            [
                1430206,
                1269656,
                509936,
                857029,
                522933,
                86194,
                31080,
                37362,
                102249,
                35718,
                349,
                347,
                1789,
                237,
                2224,
            ],
            [57, 51, 20, 34, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ),
        (
            2006,
            [
                "ÖVP",
                "SPÖ",
                "FPÖ",
                "GRÜNE",
                "BZÖ",
                "KPÖ",
                "MATIN",
                "NFÖ",
                "IVE",
                "STARK",
                "SAU",
                "SLP",
            ],
            [
                1616493,
                1663986,
                519598,
                520130,
                193539,
                47578,
                131688,
                10594,
                592,
                312,
                1514,
                2257,
            ],
            [66, 68, 21, 21, 7, 0, 0, 0, 0, 0, 0, 0],
        ),
        (
            2002,
            ["SPÖ", "FPÖ", "ÖVP", "GRÜNE", "KPÖ", "LIF", "DD", "CWG", "SLP"],
            [1792499, 491328, 2076833, 454980, 27568, 48083, 2439, 2009, 3906],
            [69, 18, 79, 17, 0, 0, 0, 0, 0],
        ),
        (
            1999,
            ["SPÖ", "ÖVP", "FPÖ", "LIF", "GRÜNE", "KPÖ", "DU", "NEIN", "CWG"],
            [1532448, 1243672, 1244087, 168612, 342260, 22016, 46943, 19286, 3030],
            [65, 52, 52, 0, 14, 0, 0, 0, 0],
        ),
        (
            1995,
            ["SPÖ", "ÖVP", "FPÖ", "GRÜNE", "LIF", "NEIN", "KPÖ", "ÖNP", "DBP"],
            [1843474, 1370510, 1060377, 233208, 267026, 53176, 13938, 1634, 830],
            [71, 52, 41, 9, 10, 0, 0, 0, 0],
        ),
        (
            1994,
            [
                "SPÖ",
                "ÖVP",
                "FPÖ",
                "GRÜNE",
                "LIF",
                "VGÖ",
                "KPÖ",
                "BGÖ",
                "NEIN",
                "CWG",
                "ÖNP",
                "FG",
                "DBP",
            ],
            [
                1617804,
                1281846,
                1042332,
                338538,
                276580,
                5776,
                11919,
                2504,
                41492,
                9051,
                4209,
                482,
                581,
            ],
            [65, 52, 42, 13, 11, 0, 0, 0, 0, 0, 0, 0, 0],
        ),
    ],
)
@pytest.mark.parametrize("fractions", [True, False])
def test_austrian_elections(year, partynames, votes, officialresult, fractions):
    result = app.compute(
        "dhondt",
        votes,
        183,
        fractions=fractions,
        parties=partynames,
        threshold=0.04,
        verbose=True,
    )
    assert str(tuple(result) == tuple(officialresult))


@pytest.mark.parametrize(
    "knesset_nr, partynames, votes, officialresult, threshold",
    [
        [
            19,
            [
                "Likud Yisrael Beitenu+Habayit Hayehudi",
                "Yesh Atid+Israel Labor Party",
                "Shas+United Torah Judaism",
                "Hatenua+Meretz",
                "United Arab List",
                "Hadash+National Democratic Assembly - Balad",
                "Kadima",
            ],
            [
                885163 + 345985,
                543458 + 432118,
                331868 + 195892,
                189167 + 172403,
                138450,
                113439 + 97030,
                78974,
            ],
            [31 + 12, 19 + 15, 11 + 7, 6 + 6, 4, 4 + 3, 2],
            0.02,
        ],
        [
            20,
            [
                "Likud Chaired by Benjamin Netanyahu for Prime Minister+Habayit Hayehudi Chaired by Naftali Bennett",
                "Zionist Camp Chaired by Isaac Herzog and Tzipi Livni+Israel's Left",
                "Joint List (Hadash, National Democratic Assembly, Arab Movement for Renewal, United Arab List)",
                "Yesh Atid Chaired by Yair Lapid",
                "Kulanu Chaired by Moshe Kahlon+Yisrael Beitenu Chaired by Avigdor Liberman",
                "Shas+United Torah Judaism",
            ],
            [
                985408 + 283910,
                786313 + 165529,
                446583,
                371602,
                315360 + 214906,
                241613 + 210143,
            ],
            [30 + 8, 24 + 5, 13, 11, 10 + 6, 7 + 6],
            0.0325,
        ],
        [
            21,
            [
                "Likud Chaired by Benjamin Netanyahu for Prime Minister+United Right",
                "Blue and White",
                "Shas+United Torah Judaism",
                "Hadash-Ta'al+Ra'am-Balad",
                "Israeli Labor Party+Meretz",
                "Yisrael Beitenu",
                "Kulanu Chaired by Moshe Kahlon",
            ],
            [
                1140370 + 159468,
                1125881,
                258275 + 249049,
                193442 + 143666,
                190870 + 156473,
                173004,
                152756,
            ],
            [35 + 5, 35, 8 + 8, 6 + 4, 6 + 4, 5, 4],
            0.0325,
        ],
        [
            22,
            [
                "Blue and White+Yisrael Beitenu",
                "Likud+Yemina",
                "Joint List (Hadash, Ra'am, Ta'al, Balad)",
                "Shas+United Torah Judaism",
                "Labor-Gesher+Democratic Union",
            ],
            [
                1151214 + 310154,
                1113617 + 260655,
                470211,
                330199 + 268775,
                212782 + 192495,
            ],
            [33 + 8, 32 + 7, 13, 9 + 7, 6 + 5],
            0.0325,
        ],
    ],
)
@pytest.mark.parametrize("fractions", [True, False])
def test_israeli_elections(
    knesset_nr, partynames, votes, officialresult, threshold, fractions
):
    print("Knesset #" + str(knesset_nr) + ":")
    result = app.compute(
        "dhondt",
        votes,
        sum(officialresult),
        fractions=fractions,
        parties=partynames,
        threshold=threshold,
        verbose=True,
    )
    assert str(tuple(result) == tuple(officialresult))
