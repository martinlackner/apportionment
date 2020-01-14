from __future__ import print_function
import sys
sys.path.insert(0, '..')
import apportionment

with open("./knesset.txt", "r") as f:

    for line in f:
        knesset_nr, partynames, votes, officialresult, threshold = \
            eval(line)
        print("Knesset #" + str(knesset_nr) + ":")
        result = apportionment.method("dhondt", votes,
                                      sum(officialresult),
                                      parties=partynames,
                                      threshold=None,  # is already excluded from input
                                      verbose=True)
        # actual results
        print("Identical with official result: "
              + (str(tuple(result) == tuple(officialresult)))
              + "\n\n")
