=======================
1. Multiples of 3 and 5
=======================

**29 Aug 2016**

`From Project Euler <https://projecteuler.net/problem=1>`__

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.

--------
Solution
--------

.. code-block:: python

    def sum_of_multiples(*multiples, maximum=10):
        multiples_sum = 0
        for i in range(maximum):
            for multiple in multiples:
                if i % multiple == 0:
                    multiples_sum += i
                    break
        return multiples_sum

    >>> sum_of_multiples(3, 5, maximum=1000)
    233168
          
