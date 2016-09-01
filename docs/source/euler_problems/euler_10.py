def prime_sum_original(n):
    """
    from: http://code.jasonbhill.com/sage/project-euler-problem-10/
    this sieve based on the 3rd block in:
        http://code.jasonbhill.com/python/project-euler-problem-7/
    """
    if n % 2 == 0:
        n += 1
    primes = [True] * n
    primes[0], primes[1] = [None] * 2
    sum = 0
    for ind, val in enumerate(primes):
        if val is True and ind > n ** 0.5 + 1:
            sum += ind
        elif val is True:
            primes[ind*2::ind] = [False] * (((n - 1)//ind) - 1)
            sum += ind
    return sum


def prime_sum(n):
    """
    Treat the indexes of a list with length == n as an indicator for
    whether that idx should be counted towards the sum of n.

    As we start from 2, discount all multiples of 2 in the sum w/ a
    slice-reassignment:

        >>> primes[idx*2::idx] = [False for i in range((((n-1//idx) - 1)))]
    
    e.g.
        >>> # Overwrite all the multiples of 2 w/ X
        >>> "0123456789"[2::2] = [i for i in range(5)]
        "01X3X5X7X9"
        >>> # Overwrite all the multiples of 3 w/ X
        >>> "01X3X5X7X9"[3::3] = [i for i in range(3)]
        "01XXX5X7XX"

    If a False number is encountered, it is not added to the total

    This is based on the "Sieve or Eratostenes". There's a fantastic graphic
    for it on Wikipedia. https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    """
    primes = [True for i in range(n)]
    primes[0], primes[1] = None, None  # don't count 0 & 1

    total = 0
    for idx in range(len(primes)):
        if idx > n//2 + 1 and primes[idx] is True :
            # There are no multiples of this prime number above half range
            total += idx
        elif primes[idx] is True:
            total += idx
            # Set all multiples of this prime in the range to not be counted
            primes[idx*2::idx] = [False for i in range((((n - 1)//idx) - 1))]
        else:
            # Do NOT count any numbers in this list that have been set to False
            continue

    return total


if __name__ == "__main__":
    print("Sum of all primes before 10:", prime_sum(10))
    print("Sum of all primes before 2000000:", prime_sum(2000000))
    print("Sum of all primes before 9999999:", prime_sum(9999999))

