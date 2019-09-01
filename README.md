# A Python implementation of common apportionment methods

This is a collection of common apportionment methods. Apportionment has two main applications: 
to assign a fixed number of [parliamentary seats to parties](https://en.wikipedia.org/wiki/Party-list_proportional_representation) (proportionally to their vote count), and to assign
[representatives in a senate to states](https://en.wikipedia.org/wiki/United_States_congressional_apportionment) (proportionally to their population count). 
A recommendable overview of apportionment methods can be found in the book "Fair Representation" by Balinski and Young [2].

The following apportionment methods are implemented:
* the largest remainder method (or Hamilton method)
* the class of divisor methods including
   - D'Hondt (or Jefferson)
   - Sainte-Laguë (or Webster)
   - Huntington-Hill
   - Adams
* the quota method [1]

This module supports Python >= 2.7 and uses [gmpy2](https://gmpy2.readthedocs.io/) if available.

## How-to

The following example calculates the seat distribution of Austrian representatives in the 
European Parliament based on the D'Hondt method and the [2019 election results](https://www.bmi.gv.at/412/Europawahlen/Europawahl_2019). Parties that received less than 4% are excluded from obtaining seats and are thus excluded in the calculation.

```python
import apportionment
parties = ['ÖVP', 'SPÖ', 'FPÖ', 'GRÜNE', 'NEOS']
distribution = [1305956, 903151, 650114, 532193, 319024]
seats = 18
apportionment.method("dhondt", distribution, seats, parties, verbose=True)
```

Another example can be found in [example.py](example.py).

## References

[1] Balinski, M. L., & Young, H. P. (1975). The quota method of apportionment. The American Mathematical Monthly, 82(7), 701-730.

[2] Balinski, M. L., & Young, H. P. (1982). Fair Representation: Meeting the Ideal of One Man, One Vote. Yale University Press, 1982. (There is a second edition from 2001 by Brookings Institution Press.)
