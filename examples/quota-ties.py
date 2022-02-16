import apportionment.methods as app

"""
Dominik's remark:
It is actually not without loss of generality to focus just on ties that still appear in the end.
Here is an example: votes = [720, 720, 120, 120], house size h = 8. Then the quota method selects
exactly the following: 3 seats go to each of the big parties, and then choose 1 big party and 1
small party and give those a seat each. This last structure can't be captured by ties just at the
end. (In contrast, for divisor methods, the ties are always of the form "assign necessary seats
(say there are t of them), and then choose an arbitrary subset of size h - t from a specified
set S of parties".)
"""

votes = [720, 720, 120, 120]
seats = 8

print("votes: ", votes)
print(seats, "seats")

result = app.compute("quota", votes, seats, verbose=True)
