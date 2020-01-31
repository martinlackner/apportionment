from __future__ import print_function
import sys
sys.path.insert(0, '..')
import apportionment

with open("./nr_wahlen.txt", "r") as f:

    for line in f:
        year, partynames, votes, officialresult = eval(line)
        print(year)
        result = apportionment.method("dhondt", votes,
                                      183,
                                      parties=partynames,
                                      threshold=.04,
                                      verbose=True)
        # actual results
        print("Identical with official result: "
              + (str(tuple(result) == tuple(officialresult)))
              + "\n\n")
