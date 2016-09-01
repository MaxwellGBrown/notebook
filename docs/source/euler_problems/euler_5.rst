====================
5. Smallest multiple
====================

**Sept 1 2016**

`Project Euler problem <https://projecteuler.net/problem=5>`__

2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

:evenly divisible: divisible w/ no remainder

--------
Solution
--------

.. code-block:: python

    from functools import reduce
    
    def smallest_multiple(min=1, max=10):
        multiples = [i for i in range(min, max+1)]
    
        # consolidate the checking list; why check both 2 and 4 if 4 also checks for 2?
        prime_subset_multiples = list()
        for multiple in multiples:
            for base, other in zip([multiple for i in range(max)], multiples):
                if other % base == 0 and base != other and other != 1:
                    break
            else:
                prime_subset_multiples.append(multiple)
    
        # increment by the largest multiple in even form to the greatest common factor
        highest_mult = prime_subset_multiples[-1]
        gcf = reduce(lambda x, y: x * y, prime_subset_multiples)
        increment = highest_mult if highest_mult % 2 == 0 else highest_mult * 2

        for n in range(highest_mult, gcf, increment):
            if all([n % m == 0 for m in prime_subset_multiples]):
                return n
        else:
            return gcf
    
    
    
    >>> smallest_multiple(min=1, max=10)
    2520
    >>> smallest_multiple(min=1, max=20)
    232792560
