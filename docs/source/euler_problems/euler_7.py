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


if __name__ == "__main__":
    print("6th prime:", nth_prime(6))
    print("10001th prime:", nth_prime(10001))
