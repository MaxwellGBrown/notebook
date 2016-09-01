========================
6. Sum square difference
========================

**Aug 29 2016**

`Project Euler problem <https://projecteuler.net/problem=6>`__

The sum of the squares of the first ten natural numbers is,

::
    12 + 22 + ... + 102 = 385

The square of the sum of the first ten natural numbers is,

::
    (1 + 2 + ... + 10)2 = 552 = 3025

Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is ``3025 − 385 = 2640``.

Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.

--------
Solution
--------

.. code-block:: python

    def sum_of_squares(maximum=10):
        total = 0
        for i in [n**2 for n in range(maximum+1)]:
            total += i
        return total


    def square_of_sums(maximum=10):
        total = 0
        for i in range(maximum+1):
            total += i
        return total**2

    >>> square_of_sums(100) - sum_of_squares(100)
    25164150
