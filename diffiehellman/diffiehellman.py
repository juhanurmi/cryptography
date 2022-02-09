# -*- coding: utf-8 -*-
'''
Diffie-Hellman example with a realistic large prime number.

RFC 3526           MODP Diffie-Hellman groups for IKE           May 2003
https://datatracker.ietf.org/doc/html/rfc3526#section-5

4096-bit MODP Group
This group is assigned id 16.
This prime is: 2^4096 - 2^4032 - 1 + 2^64 * { [2^3966 pi] + 240904 }
'''
import os

BIG_PUBLIC_PRIME = int(
    """
      FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
      29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
      EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
      E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
      EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
      C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
      83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
      670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
      E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
      DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
      15728E5A 8AAAC42D AD33170D 04507A33 A85521AB DF1CBA64
      ECFB8504 58DBEF0A 8AEA7157 5D060C7D B3970F85 A6E1E4C7
      ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226 1AD2EE6B
      F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C
      BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31
      43DB5BFC E0FD108E 4B82D120 A9210801 1A723C12 A787E6D7
      88719A10 BDBA5B26 99C32718 6AF4E23C 1A946834 B6150BDA
      2583E9CA 2AD44CE8 DBBBC2DB 04DE8EF9 2E8EFC14 1FBECAA6
      287C5947 4E6BC05D 99B2964F A090C3A2 233BA186 515BE7ED
      1F612970 CEE2D7AF B81BDD76 2170481C D0069127 D5B05AA9
      93B4EA98 8D8FDDC1 86FFB7DC 90A6C08F 4DF435C9 34063199
      FFFFFFFF FFFFFFFF
    """.replace(' ', '').replace('\n', ''),
    16)

assert int.bit_length(BIG_PUBLIC_PRIME) == 4096 # 4096-bit prime

PUBLIC_ALFA = 2 # Public integer, {2, 3, 4, ... , p-2}
assert PUBLIC_ALFA <= (BIG_PUBLIC_PRIME - 2)
assert PUBLIC_ALFA >= 2

def bin_exp(alfa, b, prime):
    ''' Calculate exponent: alfa**b % p'''
    res = 1
    while b > 0:
        if b & 1: # Bitwise and operator copies a the last bit if it is 1
            res = (res * alfa) % prime
        alfa = (alfa * alfa) % prime
        # The b value is moved right by the number of 1 bit.
        b >>= 1 # Binary Right Shift
    assert res != 0  # Becomes 0 if g is chosen badly
    return res

def random_int(num_bytes):
    ''' Creates an integer from number of random bytes '''
    random_bytes = os.urandom(num_bytes)
    assert len(random_bytes) == num_bytes
    return int.from_bytes(random_bytes, 'big')

def gen_dh_big_num(prime):
    ''' Select random exponent {1, 2, 3, ... , p-1} '''
    num_bits = int.bit_length(prime - 1)
    num_bytes = (num_bits + 7) // 8 # Floor division / 8
    number = 0
    while number == 0:
        number = random_int(num_bytes) % prime
    assert number >= 1
    assert number <= (prime - 1)
    return number

def main():
    ''' Diffie-Hellman key exchange '''
    # Selected public prime and integer
    prime = BIG_PUBLIC_PRIME # Public large prime
    alfa = PUBLIC_ALFA # Public integer, {2, 3, 4, ... , p-2}

    # Alice calculates her number
    a = gen_dh_big_num(prime) # {1, 2, 3, ... , p-1}
    # Bob calculates his number
    b = gen_dh_big_num(prime) # {1, 2, 3, ... , p-1}

    # Then they create numbers which they are going to share
    to_bob = bin_exp(alfa, a, prime)
    to_alice = bin_exp(alfa, b, prime)

    print('Alice sends:')
    print(to_bob)
    print('\nBob sends:')
    print(to_alice)

    # Alice and Bob calculate the shared secret key
    common_secret_a = bin_exp((to_alice % prime), a, prime)
    common_secret_b = bin_exp((to_bob % prime), b, prime)
    assert common_secret_a == common_secret_b
    print('\nShared secret:')
    print(common_secret_a)

if __name__ == '__main__':
    main()
