from __future__ import print_function
import apportionment.methods as app


print("Parties with surplus-vote agreements are treated as coalitions")
print("See https://www.knesset.gov.il/lexicon/eng/seats_eng.htm\n")

with open("knesset.txt", "r") as f:

    for line in f:
        knesset_nr, partynames, votes, officialresult, threshold = \
            eval(line)
        print("Knesset #" + str(knesset_nr) + ":")
        result = app.compute("dhondt", votes,
                             sum(officialresult),
                             parties=partynames,
                             threshold=threshold,
                             verbose=True)
        # actual results
        print("Identical with official result: "
              + (str(tuple(result) == tuple(officialresult)))
              + "\n\n")
