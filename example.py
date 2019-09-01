import apportionment

distribution = [77, 22, 21, 10, 6]
seats = 10

print "distribution", "."*(25 - len("distribution")), distribution
print

print seats, "seats"
print

print "apportionament results:"
for method in ["quota", "largest_remainder", "dhondt",
               "saintelague", "huntington", "adams"]:
    result = apportionment.method(method, distribution, seats, verbose=False)
    print method, "."*(25 - len(method)), result
