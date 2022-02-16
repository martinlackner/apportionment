"""
Apportionment methods
"""

from fractions import Fraction
import math
import numpy as np
import string

METHODS = [
    "quota",
    "largest_remainder",
    "dhondt",
    "saintelague",
    "modified_saintelague",
    "huntington",
    "adams",
    "dean",
]


class TiesException(Exception):
    pass


def compute(
    method,
    votes,
    seats,
    fractions=False,
    parties=string.ascii_letters,
    threshold=None,
    tiesallowed=True,
    verbose=True,
):
    filtered_votes = apply_threshold(votes, threshold)
    if method == "quota":
        return quota(filtered_votes, seats, fractions, parties, tiesallowed, verbose)
    elif method in ["lrm", "hamilton", "largest_remainder"]:
        return largest_remainder(
            filtered_votes, seats, fractions, parties, tiesallowed, verbose
        )
    elif method in [
        "dhondt",
        "jefferson",
        "saintelague",
        "webster",
        "modified_saintelague",
        "huntington",
        "hill",
        "adams",
        "dean",
        "smallestdivisor",
        "harmonicmean",
        "equalproportions",
        "majorfractions",
        "greatestdivisors",
    ]:
        return divisor(
            filtered_votes, seats, method, fractions, parties, tiesallowed, verbose
        )
    else:
        raise NotImplementedError("apportionment method " + method + " not known")


def apply_threshold(votes, threshold):
    """Sets vote counts to 0 if threshold is not met."""
    if threshold is not None:
        v = []
        combined_votes = sum(votes)
        min_votes = combined_votes * threshold
        for vote in votes:
            if vote < min_votes:
                v.append(0)
            else:
                v.append(vote)
        return v
    else:
        return votes


def __print_results(representatives, parties):
    print("apportionment:")
    for i in range(len(representatives)):
        print("  " + str(parties[i]) + ": " + str(representatives[i]))


# verifies whether a given assignment of representatives
# is within quota
def within_quota(votes, representatives, parties=string.ascii_letters, verbose=True):
    n = sum(votes)
    seats = sum(representatives)
    within = True
    for i in range(len(votes)):
        upperquota = int(math.ceil(float(votes[i]) * seats / n))
        if representatives[i] > upperquota:
            if verbose:
                print(
                    "upper quota of party",
                    parties[i],
                    "violated: quota is",
                    float(votes[i]) * seats / n,
                    "but has",
                    representatives[i],
                    "representatives",
                )
            within = False
        lowerquota = int(math.floor(float(votes[i]) * seats / n))
        if representatives[i] < lowerquota:
            if verbose:
                print(
                    "lower quota of party",
                    parties[i],
                    "violated: quota is",
                    float(votes[i]) * seats / n,
                    "but has only",
                    representatives[i],
                    "representatives",
                )
            within = False
    return within


# Largest remainder method (Hamilton method)
def largest_remainder(
    votes,
    seats,
    fractions=False,
    parties=string.ascii_letters,
    tiesallowed=True,
    verbose=True,
):
    # votes = np.array(votes)
    if verbose:
        print("\nLargest remainder method with Hare quota (Hamilton)")
    if fractions:
        q = Fraction(int(sum(votes)), seats)
        quotas = [Fraction(int(p), q) for p in votes]
        representatives = np.array(
            [int(qu.numerator // qu.denominator) for qu in quotas]
        )
    else:
        votes = np.array(votes)
        quotas = (votes * seats) / np.sum(votes)
        representatives = np.int_(np.trunc(quotas))

    ties = False
    if np.sum(representatives) < seats:
        remainders = quotas - representatives
        cutoff = remainders[np.argsort(remainders)[np.sum(representatives) - seats]]
        tiebreaking_message = (
            "  tiebreaking in order of: "
            + str(parties[: len(votes)])
            + "\n  ties broken in favor of: "
        )
        for i in range(len(votes)):
            reps_sum = np.sum(representatives)
            if reps_sum == seats and remainders[i] >= cutoff:
                if not ties:
                    tiebreaking_message = tiebreaking_message[:-2]
                    tiebreaking_message += "\n  to the disadvantage of: "
                    ties = True
                tiebreaking_message += parties[i] + ", "
            elif reps_sum < seats and remainders[i] > cutoff:
                representatives[i] += 1
            elif reps_sum < seats and remainders[i] == cutoff:
                tiebreaking_message += parties[i] + ", "
                representatives[i] += 1
        if ties and verbose:
            print(tiebreaking_message[:-2])

    if ties and not tiesallowed:
        raise TiesException("Tie occurred")

    if verbose:
        __print_results(representatives, parties)

    return representatives.tolist()


# Divisor methods
def divisor(
    votes,
    seats,
    method,
    fractions=False,
    parties=string.ascii_letters,
    tiesallowed=True,
    verbose=True,
):
    votes = np.array(votes)
    representatives = np.zeros(len(votes), dtype=int)
    if method in ["dhondt", "jefferson", "greatestdivisors"]:
        if verbose:
            print("\nD'Hondt (Jefferson) method")
        divisors = np.arange(seats) + 1
    elif method in ["saintelague", "webster", "majorfractions"]:
        if verbose:
            print("\nSainte Lague (Webster) method")
        divisors = 2 * np.arange(seats) + 1
    elif method in ["modified_saintelague"]:
        if verbose:
            print("\nModified Sainte Lague (Webster) method")
        divisors = np.insert(2 * np.arange(1.0, seats) + 1, 0, 1.4)
    elif method in ["huntington", "hill", "equalproportions"]:
        if verbose:
            print("\nHuntington-Hill method")
        if seats < len(votes):
            representatives = __divzero_fewerseatsthanparties(
                votes, seats, parties, tiesallowed, verbose
            )
        else:
            representatives = np.where(votes > 0, 1, 0)
            divisors = np.arange(seats)
            divisors = np.sqrt((divisors + 1) * (divisors + 2))
    elif method in ["adams", "smallestdivisor"]:
        if verbose:
            print("\nAdams method")
        if seats < len(votes):
            representatives = __divzero_fewerseatsthanparties(
                votes, seats, parties, tiesallowed, verbose
            )
        else:
            representatives = np.where(votes > 0, 1, 0)
            divisors = np.arange(seats) + 1
    elif method in ["dean", "harmonicmean"]:
        if verbose:
            print("\nDean method")
        if seats < len(votes):
            representatives = __divzero_fewerseatsthanparties(
                votes, seats, parties, tiesallowed, verbose
            )
        else:
            representatives = np.array([1 if p > 0 else 0 for p in votes])
            if fractions:
                divisors = np.array(
                    [
                        Fraction(2 * (i + 1) * (i + 2), 2 * (i + 1) + 1)
                        for i in range(seats)
                    ]
                )
            else:
                divisors = np.arange(seats)
                divisors = (2 * (divisors + 1) * (divisors + 2)) / (
                    2 * (divisors + 1) + 1
                )
    else:
        raise NotImplementedError("divisor method " + method + " not known")
    # assigning representatives
    if seats > np.sum(representatives):
        if fractions and method not in ["huntington", "hill", "modified_saintelague"]:
            weights = np.array(
                [[Fraction(int(p), d) for d in divisors.tolist()] for p in votes]
            )
            flatweights = sorted([w for l in weights for w in l])
        else:
            weights = np.array([p / divisors for p in votes])
            flatweights = np.sort(weights, axis=None)
        minweight = flatweights[-seats + np.sum(representatives)]

        representatives += np.count_nonzero(weights > minweight, axis=1)

    ties = False
    # dealing with ties
    if seats > np.sum(representatives):
        tiebreaking_message = (
            "  tiebreaking in order of: "
            + str(parties[: len(votes)])
            + "\n  ties broken in favor of: "
        )
        for i in range(len(votes)):
            if np.sum(representatives) == seats and minweight in weights[i]:
                if not ties:
                    if not tiesallowed:
                        raise TiesException("Tie occurred")
                    tiebreaking_message = tiebreaking_message[:-2]
                    tiebreaking_message += "\n  to the disadvantage of: "
                    ties = True
                tiebreaking_message += parties[i] + ", "
            if np.sum(representatives) < seats and minweight in weights[i]:
                tiebreaking_message += parties[i] + ", "
                representatives[i] += 1
        if ties and verbose:
            print(tiebreaking_message[:-2])

    if ties and not tiesallowed:
        raise TiesException("Tie occurred")

    if verbose:
        __print_results(representatives, parties)

    return representatives.tolist()


# required for methods with 0 divisors (Adams, Huntington-Hill)
def __divzero_fewerseatsthanparties(votes, seats, parties, tiesallowed, verbose):
    representatives = np.zeros(len(votes), dtype=int)
    if verbose:
        print(
            "  fewer seats than parties; "
            + str(seats)
            + " strongest parties receive one seat"
        )
    tiebreaking_message = "  ties broken in favor of: "
    ties = False
    mincount = np.sort(votes)[-seats]
    for i in range(len(votes)):
        if np.sum(representatives) < seats and votes[i] >= mincount:
            if votes[i] == mincount:
                tiebreaking_message += parties[i] + ", "
            representatives[i] = 1
        elif np.sum(representatives) == seats and votes[i] >= mincount:
            if not ties:
                tiebreaking_message = tiebreaking_message[:-2]
                tiebreaking_message += "\n  to the disadvantage of: "
                ties = True
            tiebreaking_message += parties[i] + ", "
    if ties and not tiesallowed:
        raise TiesException("Tie occurred")
    if ties and verbose:
        print(tiebreaking_message[:-2])
    return representatives


def quota(
    votes,
    seats,
    fractions=False,
    parties=string.ascii_letters,
    tiesallowed=True,
    verbose=True,
):
    """The quota method
    see Balinski, M. L., & Young, H. P. (1975).
    The quota method of apportionment.
    The American Mathematical Monthly, 82(7), 701-730.)

    Warning: tiesallowed is not supported here (difficult to implement)
    """
    if not tiesallowed:
        raise NotImplementedError(
            "parameter tiesallowed not supported for Quota method"
        )
    if verbose:
        print("\nQuota method")

    votes = np.array(votes)
    representatives = np.zeros(len(votes), dtype=int)

    while np.sum(representatives) < seats:
        if fractions:
            quotas = [
                Fraction(int(votes[i]), int(representatives[i]) + 1)
                for i in range(len(votes))
            ]
        else:
            quotas = votes / (representatives + 1)
        # check if upper quota is violated
        upperquota = votes * (np.sum(representatives) + 1) / np.sum(votes)
        upperquota = np.trunc(np.ceil(upperquota))
        quotas = np.where(representatives >= upperquota, 0, quotas)
        maxquotas = np.nonzero(quotas == quotas.max())[0]

        nextrep = maxquotas[0]

        # print tiebreaking information
        if verbose and len(maxquotas) > 1:
            print(
                "tiebreaking necessary in round "
                + str(np.sum(representatives) + 1)
                + ":"
                + "  tiebreaking in order of: "
                + str(parties[: len(votes)])
                + "\n  ties broken in favor of: "
                + str(parties[nextrep])
                + "\n  to the disadvantage of: "
                + ", ".join(parties[i] for i in maxquotas[1:])
            )

        representatives[nextrep] += 1

    if verbose:
        __print_results(representatives, parties)

    return representatives.tolist()
