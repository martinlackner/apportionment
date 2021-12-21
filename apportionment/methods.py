# Apportionment methods


from __future__ import print_function, division
import string
import math
from fractions import Fraction


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
    parties=string.ascii_letters,
    threshold=None,
    tiesallowed=True,
    verbose=True,
):
    filtered_votes = apply_threshold(votes, threshold)
    if method == "quota":
        return quota(filtered_votes, seats, parties, tiesallowed, verbose)
    elif method in ["lrm", "hamilton", "largest_remainder"]:
        return largest_remainder(filtered_votes, seats, parties, tiesallowed, verbose)
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
        return divisor(filtered_votes, seats, method, parties, tiesallowed, verbose)
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
    votes, seats, parties=string.ascii_letters, tiesallowed=True, verbose=True
):
    if verbose:
        print("\nLargest remainder method with Hare quota (Hamilton)")
    q = Fraction(sum(votes), seats)
    quotas = [Fraction(p, q) for p in votes]
    representatives = [int(qu.numerator) // int(qu.denominator) for qu in quotas]

    ties = False
    if sum(representatives) < seats:
        remainders = [a - b for a, b in zip(quotas, representatives)]
        cutoff = sorted(remainders, reverse=True)[seats - sum(representatives) - 1]
        tiebreaking_message = (
            "  tiebreaking in order of: "
            + str(parties[: len(votes)])
            + "\n  ties broken in favor of: "
        )
        for i in range(len(votes)):
            if sum(representatives) == seats and remainders[i] >= cutoff:
                if not ties:
                    tiebreaking_message = tiebreaking_message[:-2]
                    tiebreaking_message += "\n  to the disadvantage of: "
                    ties = True
                tiebreaking_message += parties[i] + ", "
            elif sum(representatives) < seats and remainders[i] > cutoff:
                representatives[i] += 1
            elif sum(representatives) < seats and remainders[i] == cutoff:
                tiebreaking_message += parties[i] + ", "
                representatives[i] += 1
        if ties and verbose:
            print(tiebreaking_message[:-2])

    if ties and not tiesallowed:
        raise TiesException("Tie occurred")

    if verbose:
        __print_results(representatives, parties)

    return representatives


# Divisor methods
def divisor(
    votes, seats, method, parties=string.ascii_letters, tiesallowed=True, verbose=True
):
    representatives = [0] * len(votes)
    if method in ["dhondt", "jefferson", "greatestdivisors"]:
        if verbose:
            print("\nD'Hondt (Jefferson) method")
        divisors = [i + 1 for i in range(seats)]
    elif method in ["saintelague", "webster", "majorfractions"]:
        if verbose:
            print("\nSainte Lague (Webster) method")
        divisors = [2 * i + 1 for i in range(seats)]
    elif method in ["modified_saintelague"]:
        if verbose:
            print("\nModified Sainte Lague (Webster) method")
        divisors = [1.4] + [2 * i + 1 for i in range(1, seats)]
    elif method in ["huntington", "hill", "equalproportions"]:
        if verbose:
            print("\nHuntington-Hill method")
        if seats < len(votes):
            representatives = __divzero_fewerseatsthanparties(
                votes, seats, parties, tiesallowed, verbose
            )
        else:
            representatives = [1 if p > 0 else 0 for p in votes]
            divisors = [math.sqrt((i + 1) * (i + 2)) for i in range(seats)]
    elif method in ["adams", "smallestdivisor"]:
        if verbose:
            print("\nAdams method")
        if seats < len(votes):
            representatives = __divzero_fewerseatsthanparties(
                votes, seats, parties, tiesallowed, verbose
            )
        else:
            representatives = [1 if p > 0 else 0 for p in votes]
            divisors = [i + 1 for i in range(seats)]
    elif method in ["dean", "harmonicmean"]:
        if verbose:
            print("\nDean method")
        if seats < len(votes):
            representatives = __divzero_fewerseatsthanparties(
                votes, seats, parties, tiesallowed, verbose
            )
        else:
            representatives = [1 if p > 0 else 0 for p in votes]
            divisors = [
                Fraction(2 * (i + 1) * (i + 2), 2 * (i + 1) + 1) for i in range(seats)
            ]
    else:
        raise NotImplementedError("divisor method " + method + " not known")

    # assigning representatives
    if seats > sum(representatives):
        weights = []
        for p in votes:
            if method in ["huntington", "hill", "modified_saintelague"]:
                weights.append([(p / div) for div in divisors])
            else:
                weights.append([Fraction(p, div) for div in divisors])
        flatweights = sorted([w for l in weights for w in l], reverse=True)
        minweight = flatweights[seats - sum(representatives) - 1]

        for i in range(len(votes)):
            representatives[i] += len([w for w in weights[i] if w > minweight])

    ties = False
    # dealing with ties
    if seats > sum(representatives):
        tiebreaking_message = (
            "  tiebreaking in order of: "
            + str(parties[: len(votes)])
            + "\n  ties broken in favor of: "
        )
        for i in range(len(votes)):
            if sum(representatives) == seats and minweight in weights[i]:
                if not ties:
                    if not tiesallowed:
                        raise TiesException("Tie occurred")
                    tiebreaking_message = tiebreaking_message[:-2]
                    tiebreaking_message += "\n  to the disadvantage of: "
                    ties = True
                tiebreaking_message += parties[i] + ", "
            if sum(representatives) < seats and minweight in weights[i]:
                tiebreaking_message += parties[i] + ", "
                representatives[i] += 1
        if ties and verbose:
            print(tiebreaking_message[:-2])

    if ties and not tiesallowed:
        raise TiesException("Tie occurred")

    if verbose:
        __print_results(representatives, parties)

    return representatives


# required for methods with 0 divisors (Adams, Huntington-Hill)
def __divzero_fewerseatsthanparties(votes, seats, parties, tiesallowed, verbose):
    representatives = [0] * len(votes)
    if verbose:
        print(
            "  fewer seats than parties; "
            + str(seats)
            + " strongest parties receive one seat"
        )
    tiebreaking_message = "  ties broken in favor of: "
    ties = False
    mincount = sorted(votes, reverse=True)[seats - 1]
    for i in range(len(votes)):
        if sum(representatives) < seats and votes[i] >= mincount:
            if votes[i] == mincount:
                tiebreaking_message += parties[i] + ", "
            representatives[i] = 1
        elif sum(representatives) == seats and votes[i] >= mincount:
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


def quota(votes, seats, parties=string.ascii_letters, tiesallowed=True, verbose=True):
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
    representatives = [0] * len(votes)
    while sum(representatives) < seats:
        quotas = [Fraction(votes[i], representatives[i] + 1) for i in range(len(votes))]
        # check if upper quota is violated
        for i in range(len(votes)):
            upperquota = int(
                math.ceil(float(votes[i]) * (sum(representatives) + 1) / sum(votes))
            )
            if representatives[i] >= upperquota:
                quotas[i] = 0

        maxquotas = [i for i in range(len(votes)) if quotas[i] == max(quotas)]

        nextrep = maxquotas[0]

        # print tiebreaking information
        if verbose and len(maxquotas) > 1:
            print(
                "tiebreaking necessary in round "
                + str(sum(representatives) + 1)
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

    return representatives
