================
7. 10001st prime
================

**1 Sept 2016**

`Project Euler problem <https://projecteuler.net/problem=7>`__

By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10 001st prime number?

--------
Solution
--------

.. code-block:: python

    def is_prime(n):
        for i in range(2, int(n//2 + 1)):
            if n % i == 0:
                return False
        else:
            return True
    
    def nth_prime(n):
        prime_counter, k = 0, 1
        while prime_counter < n:
            k += 1
            if is_prime(k) is True:
                prime_counter += 1
        return k
    
    
    >>> nth_prime(6)
    13
    >>> nth_prime(10001)
    104743
