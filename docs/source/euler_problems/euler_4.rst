=============================
4. Largest palindrome product
=============================

**Aug 29 2016**

`Project Euler problem <https://projecteuler.net/problem=4>`__

A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.


--------
Solution
--------

.. code-block:: python

    def largest_palindromic_number_by_digit(digits=2):
        large = 0
        for i in range(10 ** digits -1, 10 ** (digits-1), -1):
            for k in range(10 ** digits -1, 10 ** (digits-1), -1):
                product = i * k
                str_product = str(product)
                if str_product == str_product[::-1] and product > large:
                    large = product
        return large

    >>> largest_palindromic_number_by_digit(3)
    906609
            
