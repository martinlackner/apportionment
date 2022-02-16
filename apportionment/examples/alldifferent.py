# Find vote distribution that produces a different apportionments
# for each of the specified apportionment methods


from __future__ import print_function
import apportionment.methods as app
from itertools import combinations


maxvoters = 20
parties = 5
seats = 20
methods = ["quota", "largest_remainder", "dhondt", "saintelague", "adams"]


iterator = combinations(range(1, maxvoters + 1), parties)

for iterations, votes in enumerate(iterator):
    apportionments = set()

    for method in methods:
        apportionments.add(
                tuple(
                    app.compute(method, votes, seats, verbose=False)
                )
            )

    if len(apportionments) == len(methods):
        break
else:
    print("No vote distribution found within the parameter range.")
    quit()

print("votes = {}".format(votes))
print("found in {} iterations\n\n".format(iterations))

for method in methods:
    print(
        "{:>20s}: {}".format(method, app.compute(method, votes, seats, verbose=False))
    )
