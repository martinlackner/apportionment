# Find vote distribution that produces a different apportionments
# for each of the specified apportionment methods

import apportionment.methods as app
from itertools import combinations


maxvoters = 20
parties = 5
seats = 20
methods = ["quota", "largest_remainder", "dhondt", "saintelague", "adams"]

for iterations, votes in enumerate(combinations(range(1, maxvoters + 1), parties)):
    apportionments = set()

    for method in methods:
        apportionments.add(tuple(app.compute(method, votes, seats, verbose=False)))

    if len(apportionments) == len(methods):
        break
else:
    print("No vote distribution found within the parameter range.")
    quit()

print("votes = {}".format(votes))
print("found in {} iterations\n\n".format(iterations))

for method in methods:
    print("{:>20s}: {}".format(method, app.compute(method, votes, seats, verbose=False)))
