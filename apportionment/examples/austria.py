from __future__ import print_function
import apportionment.methods as app


with open("./nr_wahlen.txt", "r") as f:

    for line in f:
        year, partynames, votes, officialresult = eval(line)
        print(year)
        result = app.compute(
            "dhondt", votes, 183, parties=partynames, threshold=0.04, verbose=True
        )
        # actual results
        print(
            "Identical with official result: "
            + (str(tuple(result) == tuple(officialresult)))
            + "\n\n"
        )
