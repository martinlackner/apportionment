from __future__ import print_function
import sys
sys.path.insert(0, '..')
import apportionment

with open("./nr_wahlen.txt", "r") as f:

    for line in f:
        result = eval(line)
        print(result[0])
        print(apportionment.method("dhondt", result[2],
                                   sum(result[3]),
                                   parties=result[1],
                                   threshold=.04,
                                   verbose=False))
        # actual results
        print(result[3])
