=======================
10. Summation of primes
=======================

**1 Sept 2016**

`Project Euler problem <https://projecteuler.net/problem=10>`__

The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.


--------
Solution
--------

Whether from fatigue of simple mindedness, I had a hard time answering this
one. 

After some thought I decided to seek a solution. And, as such for not having
solved it on my own, I must now over-explain the answer so I'll never forget
it.


+++++++++++++++
Initial Attempt
+++++++++++++++

As usual, I tried the most simple answer first to see how well it worked.

.. code-block:: python

    def is_prime(n):
        for i in range(2, int(n//2 + 1)):
            if n % i == 0:
                return False
        else:
            return True


    def prime_sum(n):
        total = 0
        for i in range(1, n+1):
            if is_prime(i):
                total += i
        return total


... I never saw the completion. My impatience had me Ctrl+C'ing every time.


+++++++++++++
Pseudo Primes
+++++++++++++

My 2nd implementation had the concept of `pseudoprimes <https://en.wikipedia.org/wiki/Fermat_pseudoprime>`__ and `Fermat's primality test <https://en.wikipedia.org/wiki/Fermat_primality_test>`__.

The concept being that you could most-often determine that a number was **not**
prime, and if it was somewhat conclusive (but not difinitive!) on whether a
number was a prime.

::
  
  # with any base number a > 1
  if a**(n-1) % n != 1 % n then n is NOT prime

However, adding in this check before actually running the iteration did little
to speed up processing.


++++++++++++++++++++++++++++++
Just give me the answer damnit
++++++++++++++++++++++++++++++

After avoiding answers and losing all hope I found `a very sloppy yet efficient
solution <http://code.jasonbhill.com/sage/project-euler-problem-10/>`__.

.. code-block:: python

    def prime_sum_original(n):
        """ from: http://code.jasonbhill.com/sage/project-euler-problem-10/ """
        if n % 2 == 0:
            n += 1
        primes = [True] * n
        primes[0], primes[1] = [None], [None]
        sum = 0
        for ind, val in enumerate(primes):
            if val is True and ind > n ** 0.5 + 1:
                sum += ind
            elif val is True:
                primes[ind*2::ind] = [False] * (((n - 1)//ind) - 1)
                sum += ind
        return sum

This answer leverages the `Sieve of Eratostenes <https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes>`__.

So after dissecting what was actually happening I cleaned up the code, added
comments for any non-sievers out there, and modernized it:

.. code-block:: python


    def prime_sum(n):
        sieve = [True for i in range(n)]
        sieve[0], sieve[1] = None, None  # don't count 0 & 1

        total = 0
        for idx in range(len(sieve)):
            if idx > n//2 + 1 and sieve[idx] is True :
                # There are no multiples of this prime number above half range
                total += idx
            elif sieve[idx] is True:
                total += idx
                # Set all multiples of this prime in the range to not be counted
                sieve[idx*2::idx] = [False for i in range((((n - 1)//idx) - 1))]
            else:
                # Do NOT count any numbers in this list that have been set to False
                continue

        return total

    >>> prime_sum(10)
    17
    >>> prime_sum(2000000)
    142913828922

-------
Summary
-------

* Using sieves in real-integer series can speed things up significantly
* Assignment to sliced objects is a thing ``sieve[idx::idx] = [False, False,...]``
