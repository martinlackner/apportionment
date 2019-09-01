from gmpy2 import mpq as mpq
import string
import math

def method(method, distribution, seats, parties=string.ascii_uppercase, verbose=True):
    if method == "quota":
        return quota(distribution, seats, parties, verbose)
    elif method in ["lrm","hamilton","largest_remainder"]:
        return largest_remainder(distribution, seats, parties, verbose)
    elif method in ["dhondt","jefferson","saintelague","webster","huntington","hill","adams"]:
        return divisor(distribution, seats, method, parties, verbose)
    else:
        print "method",method,"unknown"
        quit()

# required for methods with 0 divisors (Adams, Huntington-Hill)
def __divzero_fewerseatsthanparties(distribution, seats, parties, verbose):
    representatives = [0] * len(distribution)
    if verbose:
        print "  fewer seats than parties; "+str(seats)+" strongest parties receive one seat"
    tiebreaking_message = "  ties broken in favor of: "
    ties = False
    mincount = sorted(distribution,reverse=True)[seats-1]
    for i in range(len(distribution)):
        if sum(representatives) < seats and distribution[i] >= mincount:
            if distribution[i] == mincount:
                tiebreaking_message += parties[i] + ", "
            representatives[i] = 1
        elif sum(representatives) == seats and distribution[i] >= mincount:
            if not ties:
                tiebreaking_message = tiebreaking_message[:-2]
                tiebreaking_message += "\n  to the disadvantage of: "
                ties = True
            tiebreaking_message += parties[i] + ", "
    if ties and verbose:
        print tiebreaking_message[:-2]
    return representatives
    
def __print_results(representatives, parties):
    for i in range(len(representatives)):
        print "  "+str(parties[i])+": "+str(representatives[i])

def within_quota(distribution, seats, representatives, parties=string.ascii_uppercase):
    n = sum(distribution)
    within = True
    for i in range(len(distribution)):
        if representatives[i] > math.ceil(float(distribution[i]) * seats / n):
            print "upper quota of party",parties[i],"violated: quota is",float(distribution[i]) * seats / n,"but has", representatives[i],"representatives"  
            within=False
        if representatives[i] < math.floor(float(distribution[i]) * seats / n):
            print "lower quota of party",parties[i],"violated: quota is",float(distribution[i]) * seats / n,"but has only", representatives[i],"representatives"   
            within = False
    return within

# Largest remainder method (Hamilton method)
def largest_remainder(distribution, seats, parties=string.ascii_uppercase, verbose=True):
    if verbose:
        print "\nLargest remainder method with Hare quota (Hamilton)"
    q = mpq(sum(distribution),seats)
    quotas = [mpq(p,q) for p in distribution]
    representatives = [int(qu.numerator)//int(qu.denominator) for qu in quotas]
    if sum(representatives) < seats:
        remainders = [a-b for a,b in zip(quotas,representatives)]
        cutoff = sorted(remainders,reverse=True)[seats-sum(representatives)-1]
        tiebreaking_message = "  tiebreaking in order of: "+str(parties[:len(distribution)])+"\n  ties broken in favor of: "
        ties = False
        for i in range(len(distribution)):
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
            print tiebreaking_message[:-2]
        
    if verbose:
        __print_results(representatives, parties)
        
    return representatives


# Divisor methods
def divisor(distribution, seats, method, parties=string.ascii_uppercase, verbose=True):
    if len(distribution) > len(parties):
        parties = list(range(len(distribution)))
    representatives = [0] * len(distribution)
    if method in ["dhondt","jefferson"]:
        if verbose:
            print "\nD'Hondt (Jefferson) method"
        divisors = [i+1 for i in range(seats)] 
    elif method in ["saintelague","webster"]:
        if verbose:
            print "\nSainte Lague (Webster) method"
        divisors = [2*i+1 for i in range(seats)] 
    elif method in ["huntington","hill"]:
        if verbose:
            print "\nHuntington-Hill method"
        if seats < len(distribution):
            representatives = __divzero_fewerseatsthanparties(distribution, seats, parties, verbose)
        else:
            representatives = [1] * len(distribution)
            divisors = [math.sqrt((i+1)*(i+2)) for i in range(seats)] 
    elif method in ["adams"]:
        if verbose:
            print "\nAdams method"
        if seats < len(distribution):
            representatives = __divzero_fewerseatsthanparties(distribution, seats, parties, verbose)
        else:
            representatives = [1] * len(distribution)
            divisors = [i+1 for i in range(seats)] 
    else:
        print method,"is not a defined divisor method"
        return
    
    # assigning representatives
    if seats > sum(representatives):
        weights = []
        for p in distribution:
            weights.append([mpq(p,div) for div in divisors])
        flatweights = [w for l in weights for w in l ]
        minweight = sorted(flatweights, reverse=True)[seats-sum(representatives)-1] 
        
        for i in range(len(distribution)):
            representatives[i] += len([w for w in weights[i] if w > minweight])
    
    # dealing with ties
    if seats > sum(representatives):
        tiebreaking_message = "  tiebreaking in order of: "+str(parties[:len(distribution)])+"\n  ties broken in favor of: "
        ties = False
        for i in range(len(distribution)):
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
            print tiebreaking_message[:-2]
        
    if verbose:
        __print_results(representatives, parties)
            
    return representatives

# Quota method 
#  ( see Balinski, M. L., & Young, H. P. (1975). The quota method of apportionment.
#    The American Mathematical Monthly, 82(7), 701-730.)
def quota(distribution, seats, parties=string.ascii_uppercase, verbose=True):
    if verbose:
        print "\nQuota method"
    representatives = [0] * len(distribution)
    tied = []
    for k in range(1,seats+1):
        quotas = [mpq(distribution[i],representatives[i]+1) for i in range(len(distribution))]
        # check if upper quota is violated
        for i in range(len(distribution)):
            if representatives[i] >= math.ceil(float(distribution[i])*k/sum(distribution)):  
                quotas[i] = 0
        chosen = [i for i in range(len(distribution)) if quotas[i] == max(quotas)]
        if verbose:
            if len(chosen) > 1:
                tied.append(representatives[chosen[0]])
            else:
                tied = []
        representatives[chosen[0]] += 1
    
    # print tiebreaking information
    if verbose and len(tied) > 0:
        tiebreaking_message = "  tiebreaking in order of: "+str(parties[:len(distribution)])+"\n  ties broken in favor of: "
        for i in range(len(tied)):
            tiebreaking_message += tied[i] + ", "
        tiebreaking_message = tiebreaking_message[:-2] + "\n  to the disadvantage of: "
        for i in range(1,len(chosen)):
            tiebreaking_message += tied[i] + ", "
        print tiebreaking_message
        
    if verbose:
        __print_results(representatives, parties)
            
    return representatives 
