# -*- coding: utf-8 -*-
''' RSA example with realistic large 4096-bit prime numbers '''
import os
import random

def random_int(num_bytes):
    ''' Creates an integer from number of random bytes '''
    number = 0
    while number == 0 or int.bit_length(number) != (num_bytes * 8):
        random_bytes = os.urandom(num_bytes)
        assert len(random_bytes) == num_bytes
        number = int.from_bytes(random_bytes, 'big')
    assert int.bit_length(number) == num_bytes * 8
    return number

def miller_rabin(number, k):
    '''
    Implementation uses the Miller-Rabin Primality ideas from https://gist.github.com/Ayrx/5884790

    The probability that a random 1024-bit integer is prime is about 1/900.
    When the value is non-prime, Miller-Rabin will detect it with probability 3/4 at each round.

    See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    '''
    small_prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
    if number in small_prime_list:
        return True
    if number < 2:
        return False
    for test in small_prime_list:
        if number % test ==  0:
            return False
    r = 0
    s = number - 1
    while s % 2 == 0:
        r = r + 1
        s //= 2
    for i in range(k):
        a = random.randrange(2, number - 1)
        x = pow(a, s, number)
        if x == 1 or x == number - 1:
            continue
        for j in range(r - 1):
            x = pow(x, 2, number)
            if x == number - 1:
                break
        else:
            return False
    return True

def is_prime(number):
    ''' Call Miller-Rabin test '''
    return miller_rabin(number, k=40)

def random_prime(num_bits):
    ''' Return a num_bits bits prime number '''
    num_bytes = (num_bits + 7) // 8 # Floor division / 8
    number = 10
    while not is_prime(number):
        number = random_int(num_bytes=num_bytes)
    return number

def inverse_mod(e, phi_n):
    ''' Solve d from d * e = 1 mod phi(n) '''
    return pow(e, -1, phi_n) # Python 3.8+

def rsacrypt(k_public, message):
    ''' message**e % n '''
    n = k_public[0]
    e = k_public[1]
    return pow(message, e, n)

def main():
    ''' RSA '''
    # 1. Selected public prime and integer
    bits = 4096
    p = random_prime(num_bits=bits) # Private large prime, 4096 bits
    print('Creating a private %d-bit primary q. Takes some minutes.' % bits)
    q = random_prime(num_bits=bits) # Private large prime, 4096 bits
    print('Creating a private %d-bit primary c. Takes some minutes.' % bits)

    # 2. Compute public n = p*q
    n = p*q

    # 3. Compute phi(n) with the knowlege of factors p and q
    phi_n = (p-1)*(q-1)

    # 4. Select the public exponent e, {1, 2, ..., phi(n)-1}, such that gcd(e, phi(n)) = 1
    prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
    for prime in prime_list:
        if phi_n % prime != 0: # gcd(e, phi(n)) = 1
            e = prime
            break
    assert e < phi_n

    # 5. Compute the private key d such that d * e = 1 mod phi(n)
    d = inverse_mod(e, phi_n)
    k_private = (n, d)
    k_public = (n, e)

    print('Alice computes the private key:')
    print(k_private)

    print('Alice publishes the public key:')
    print(k_public)

    message = 1337
    print('Bob encrypts %d with the public key and sends:' % message)
    encrypted_message = rsacrypt(k_public, message)
    print(encrypted_message)

    print('Alice decrypts the message:')
    reseived_message = rsacrypt(k_private, encrypted_message)
    print(reseived_message)

    assert reseived_message == message

if __name__ == '__main__':
    main()
