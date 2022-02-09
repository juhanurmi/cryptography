# -*- coding: utf-8 -*-
'''
python3 simhash_password_test.py
'''
from simhash import Simhash

def distance(hash1, hash2):
    ''' Similarity comparison between two hashes '''
    # 0001011010100000110000000000010001000000001011001100101100011000
    # 0001011010100000110000111000010001000000001011001100101100011000
    # ----------------------^^^---------------------------------------
    # distance = 3
    return sum([1 for index, value in enumerate(hash1) if hash2[index] != value])

def simhash_value(text):
    '''
    Returns a simhash binary of the text.

    Note that collision is possible with simhash:

    1111111111111111111111111111111111111111111111111111111111111111 is product of
    VILB6XCPRPN914HQNK22PQQJREYINBNWPFJPGGXB81U6V4T5PWODMYU073024UV81E0OEKJTGTMRXOOPLWG3Z3BZQUHANA4WZFYI
    GFjgUuzRUGMihG7ha3ES2ZF3jdE0o6PnjZTkUCCNtaTAcqsMYIUywJtLqQr6fSMN4MIEumYYKdFs434WsSYkFyw7huB0vI7pJXFJ

    0000000000000000000000000000000000000000000000000000000000000000 is product of
    VBG24ZIY1YWB057P3RNTG8TUXJFK0YFAJUUSMGLEML3NL732WRXR3KJA2BJWPL6B96FCOR5WBT7ETSNANSJGP9HNSN63V5RTI16S
    1SfsDqztAeAkYDxKoG4YNSAkxMELjcjYObGSZPB0r2tglNm1MMsJ7Konf2CPp2q2kOIfgRaUSsI8JubQkraVeBhahlBrJxdfM6Vd
    '''
    return str("{0:b}".format(Simhash(text).value)).zfill(64)

def main():
    ''' Main function '''
    # Our password is salted with unique random data.
    # When the salt is unique for each user's password,
    # the attacker must compute a hash table for each user hash.
    # This creates a big bottleneck for the attacker in case the database is leaked.
    secret_salt = 'pwvr5Hm1AgqTsvJQrGOHf7uZya7w9BPsu42iB1tqYzJHendCVLlap0uxVvhgCaC9'
    original_password_hash = simhash_value('myG00Doldphrase' + secret_salt)
    new_passwords = ['myG00Doldphrase', 'myG00Doldphrase1', 'myG00Doldphrase11',
                     'myG00DoldphrasE11', 'MYG00DoldphrasE11', 'MYG00DoldphrASE11',
                     'MYG00DnewphrASE11']
    for password in new_passwords:
        new_hash = simhash_value(password + secret_salt)
        diff = distance(original_password_hash, new_hash)
        print('\nNew password candidate: %s' % password)
        print('Compare old password hash to the new password hash:')
        print(original_password_hash)
        print(new_hash)
        print('Distance is %d' % diff)
        if diff > 15: # Threshold could be 10...15
            print('New password set!')
            break
        else:
            print('Too similar password compared to the previous password.')
            print('Select a new password different from the old one.')

if __name__ == '__main__':
    main()
