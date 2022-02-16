import apportionment.methods as app

votes = [1, 3, 6, 7, 78]
seats = 20

print("votes", "." * (25 - len("votes")), votes, "\n")

print(seats, "seats", "\n")

print("apportionment results:")
for method in [
    "quota",
    "largest_remainder",
    "dhondt",
    "saintelague",
    "huntington",
    "adams",
    "dean",
]:
    result = app.compute(method, votes, seats, verbose=False)
    print(method, "." * (25 - len(method)), result)
