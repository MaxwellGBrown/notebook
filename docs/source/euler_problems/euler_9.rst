==============================
9. Special Pythagorean triplet
==============================

**1 Sept 2016**

`Project Euler problem <https://projecteuler.net/problem=9>`__

A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,

::
  a2 + b2 = c2

For example, 32 + 42 = 9 + 16 = 25 = 52.

There exists exactly **one** Pythagorean triplet for which ``a + b + c == 1000``.
Find the product *abc*.

--------
Solution
--------

.. code-block:: python

    def find_special_triplet_product():
        for a in range(1, int(1000//3)):
            for b in range(a + 1, 1000 - a):
                c = 1000 - a - b
                if a**2 + b**2 == c**2:
                    return a * b * c

    >>> find_special_triplet_product()
    31875000
