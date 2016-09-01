=======================
3. Largest prime factor
=======================

**Sept 1 2016**

`From Project Euler <https://projecteuler.net/problem=3>`__

The `prime factors <https://en.wikipedia.org/wiki/Prime_factor>`__ of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?

--------
Solution
--------

.. code-block:: python

    def is_prime(n):
        for i in range(2, int(n/2 + 1)):
            if n % i == 0:
                return False
        return True

    def primefactors(n):
        # recursion
        for i in range(2, int(n//2 +1)):
            if n % i == 0:  # if i is a factor of n...
                if is_prime(i) is True:  # if i is a prime number...
                    return [i] + primefactors(int(n//i))

        # basis-case for primes
        return [n]

    >>> primefactors(13195)
    [5, 7, 13, 29]
    >>> primefactors(600851475143)
    [71, 839, 1471, 6857]
