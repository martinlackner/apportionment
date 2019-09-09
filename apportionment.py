from __future__ import print_function, division
import string
import math
try:
    from gmpy2 import mpq as Fraction
except ImportError:
    from fractions import Fraction


def method(method, votes, seats, parties=string.ascii_uppercase,
           verbose=True):
    if method == "quota":
        return quota(votes, seats, parties, verbose)
    elif method in ["lrm", "hamilton", "largest_remainder"]:
        return largest_remainder(votes, seats, parties, verbose)
    elif method in ["dhondt", "jefferson", "saintelague", "webster",
                    "huntington", "hill", "adams"]:
        return divisor(votes, seats, method, parties, verbose)
    else:
        raise NotImplementedError("apportionment method " + method +
                                  " not known")


# required for methods with 0 divisors (Adams, Huntington-Hill)
def __divzero_fewerseatsthanparties(votes, seats, parties, verbose):
    representatives = [0] * len(votes)
    if verbose:
        print("  fewer seats than parties; " + str(seats) +
              " strongest parties receive one seat")
    tiebreaking_message = "  ties broken in favor of: "
    ties = False
    mincount = sorted(votes, reverse=True)[seats-1]
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
    if ties and verbose:
        print(tiebreaking_message[:-2])
    return representatives


def __print_results(representatives, parties):
    for i in range(len(representatives)):
        print("  "+str(parties[i])+": "+str(representatives[i]))


def within_quota(votes, seats, representatives,
                 parties=string.ascii_uppercase):
    n = sum(votes)
    within = True
    for i in range(len(votes)):
        upperquota = int(math.ceil(float(votes[i]) * seats / n))
        if representatives[i] > upperquota:
            print("upper quota of party", parties[i],
                  "violated: quota is", float(votes[i]) * seats / n,
                  "but has", representatives[i], "representatives")
            within = False
        lowerquota = int(math.floor(float(votes[i]) * seats / n))
        if representatives[i] < lowerquota:
            print("lower quota of party", parties[i],
                  "violated: quota is", float(votes[i]) * seats / n,
                  "but has only", representatives[i], "representatives")
            within = False
    return within


# Largest remainder method (Hamilton method)
def largest_remainder(votes, seats, parties=string.ascii_uppercase,
                      verbose=True):
    if verbose:
        print("\nLargest remainder method with Hare quota (Hamilton)")
    q = Fraction(sum(votes), seats)
    quotas = [Fraction(p, q) for p in votes]
    representatives = [int(qu.numerator)//int(qu.denominator) for qu in quotas]
    if sum(representatives) < seats:
        remainders = [a-b for a, b in zip(quotas, representatives)]
        cutoff = sorted(remainders, reverse=True)[seats-sum(representatives)-1]
        tiebreaking_message = ("  tiebreaking in order of: " +
                               str(parties[:len(votes)]) +
                               "\n  ties broken in favor of: ")
        ties = False
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

    if verbose:
        __print_results(representatives, parties)

    return representatives


# Divisor methods
def divisor(votes, seats, method, parties=string.ascii_uppercase,
            verbose=True):
    if len(votes) > len(parties):
        parties = list(range(len(votes)))
    representatives = [0] * len(votes)
    if method in ["dhondt", "jefferson"]:
        if verbose:
            print("\nD'Hondt (Jefferson) method")
        divisors = [i+1 for i in range(seats)]
    elif method in ["saintelague", "webster"]:
        if verbose:
            print("\nSainte Lague (Webster) method")
        divisors = [2*i+1 for i in range(seats)]
    elif method in ["huntington", "hill"]:
        if verbose:
            print("\nHuntington-Hill method")
        if seats < len(votes):
            representatives = __divzero_fewerseatsthanparties(votes,
                                                              seats, parties,
                                                              verbose)
        else:
            representatives = [1 if p > 0 else 0 for p in votes]
            divisors = [math.sqrt((i+1)*(i+2)) for i in range(seats)]
    elif method in ["adams"]:
        if verbose:
            print("\nAdams method")
        if seats < len(votes):
            representatives = __divzero_fewerseatsthanparties(votes,
                                                              seats, parties,
                                                              verbose)
        else:
            representatives = [1 if p > 0 else 0 for p in votes]
            divisors = [i+1 for i in range(seats)]
    else:
        print(method, "is not a defined divisor method")
        return

    # assigning representatives
    if seats > sum(representatives):
        weights = []
        for p in votes:
            if method in ["huntington", "hill"]:
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
        tiebreaking_message = ("  tiebreaking in order of: " +
                               str(parties[:len(votes)]) +
                               "\n  ties broken in favor of: ")
        for i in range(len(votes)):
            if sum(representatives) == seats and minweight in weights[i]:
                if not ties:
                    tiebreaking_message = tiebreaking_message[:-2]
                    tiebreaking_message += "\n  to the disadvantage of: "
                    ties = True
                tiebreaking_message += parties[i] + ", "
            if sum(representatives) < seats and minweight in weights[i]:
                tiebreaking_message += parties[i] + ", "
                representatives[i] += 1
        if ties and verbose:
            print(tiebreaking_message[:-2])

    if verbose:
        __print_results(representatives, parties)

    return representatives


# The quota method
#  ( see Balinski, M. L., & Young, H. P. (1975).
#        The quota method of apportionment.
#        The American Mathematical Monthly, 82(7), 701-730.)
def quota(votes, seats, parties=string.ascii_uppercase, verbose=True):
    if verbose:
        print("\nQuota method")
    representatives = [0] * len(votes)
    tied = []
    for k in range(1, seats+1):
        quotas = [Fraction(votes[i], representatives[i]+1)
                  for i in range(len(votes))]
        # check if upper quota is violated
        for i in range(len(votes)):
            upperquota = int(math.ceil(float(votes[i]) *
                                       k / sum(votes)))
            if representatives[i] >= upperquota:
                quotas[i] = 0
        chosen = [i for i in range(len(votes))
                  if quotas[i] == max(quotas)]
        if verbose:
            if len(chosen) > 1:
                tied.append(representatives[chosen[0]])
            else:
                tied = []
        representatives[chosen[0]] += 1

    # print tiebreaking information
    if verbose and len(tied) > 0:
        tiebreaking_message = ("  tiebreaking in order of: " +
                               str(parties[:len(votes)]) +
                               "\n  ties broken in favor of: ")
        for i in range(len(tied)):
            tiebreaking_message += tied[i] + ", "
        tiebreaking_message = (tiebreaking_message[:-2] +
                               "\n  to the disadvantage of: ")
        for i in range(1, len(chosen)):
            tiebreaking_message += tied[i] + ", "
        print(tiebreaking_message)

    if verbose:
        __print_results(representatives, parties)

    return representatives
