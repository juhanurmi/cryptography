# -*- coding: utf-8 -*-
'''
python3 work.py
'''
import random
import hashlib

def sha256_value(text):
    ''' Calculate hexdigest hash value '''
    return hashlib.sha256(str(text).encode('utf-8')).hexdigest()

def random_string(size=128):
    ''' Return a random string, default size is 128 '''
    # Letters (upper and lower cases) + digits. Total of 64 options.
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for index in range(size))

def proof_of_work(message, difficulty):
    ''' Looking a hash value according to the difficulty.
    Difficulty means the number of zeros in the beginning of the hash value. '''
    while True:
        nonsense = random_string(size=12)
        full_message = message + nonsense
        hashsum = sha256_value(full_message)
        print(hashsum)
        if hashsum[0:difficulty] == '0'*difficulty:
            print('Found a hash which starts with %s' % ('0'*difficulty))
            print('Nonsense is %s\n' % nonsense)
            break
    print(full_message)

def main():
    ''' The main function '''
    difficulty = 5 # Number of zeros in the hash value
    message = "A new block of transactions  and pointer to the previous block. + Nonsense: "
    proof_of_work(message, difficulty)

if __name__ == '__main__':
    main()
