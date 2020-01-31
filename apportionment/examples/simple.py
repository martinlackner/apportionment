from __future__ import print_function
import apportionment.methods as app

votes = [77, 22, 21, 10, 6]
seats = 10

print("votes", "."*(25 - len("votes")), votes, "\n")

print(seats, "seats", "\n")

print("apportionment results:")
for method in ["quota", "largest_remainder", "dhondt",
               "saintelague", "huntington", "adams"]:
    result = app.compute(method, votes, seats, verbose=False)
    print(method, "."*(25 - len(method)), result)
