# -*- coding: utf-8 -*-
'''
python3 salt.py
'''
import time
import random
import hashlib

def all_ip_addresses():
    ''' Return all IPv4 addresses one by one '''
    # IPv4 uses a 32-bit address space: 4,294,967,296 (2**32) unique addresses
    for part1 in range(11, 256): # 11-255
        for part2 in range(0, 256): # 0-255
            for part3 in range(0, 256): # 0-255
                for part4 in range(0, 256): # 0-255
                    yield '%s.%s.%s.%s' % (part1, part2, part3, part4)

def random_string(size=128):
    ''' Return a random string, default size is 128 '''
    # Letters (upper and lower cases) + digits. Total of 64 options.
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for index in range(size))

def sha1_value(text):
    ''' Calculate hexdigest hash value '''
    return hashlib.sha1(str(text).encode('utf-8')).hexdigest()

def main():
    ''' Main function '''
    userdata_json = {'visit1': {'ip': '11.20.242.34', 'time': '2021-12-12', 'browser': 'firefox'},
                     'visit2': {'ip': '180.130.113.100', 'time': '2021-12-15', 'browser': 'chrome'},
                     'visit3': {'ip': '180.130.113.100', 'time': '2021-12-16', 'browser': 'chrome'},
                     'visit4': {'ip': '11.20.242.34', 'time': '2021-12-20', 'browser': 'firefox'},
                     'visit5': {'ip': '11.20.242.34', 'time': '2021-12-21', 'browser': 'firefox'},
                     'visit6': {'ip': '130.236.201.188', 'time': '2021-12-23', 'browser': 'safari'},
                     'visit7': {'ip': '175.228.153.155', 'time': '2021-12-23', 'browser': 'edge'}}
    test_ip = userdata_json['visit1']['ip']
    print('Example hashing %s' % test_ip)
    plainhash = sha1_value(test_ip)
    print('Hash without salt: %s\n' % plainhash)
    time.sleep(10)
    print('Bruteforce the IP address from the plain hash...')
    starttime = time.time() # Start time
    test_count = 0
    for index, ip_address in enumerate(all_ip_addresses()):
        testhash = sha1_value(ip_address)
        print('%s \t %s' % (ip_address, testhash))
        if plainhash == testhash:
            print('Found IP address: %s' % ip_address)
            test_count = index + 1
            break
    endtime = time.time() - starttime
    print('Found match in %d seconds and %d tests/second.\n' % (endtime, int(test_count/endtime)))
    print('Create a salt+hash version of the database to hide original IP addresses.')
    # Let's use a random salt for each different IP address
    # Use the same salt for the same IP
    salt_map = {} # Structure to keep one salt per each unique IP address
    for key, userdata in userdata_json.items():
        ip_address = userdata['ip']
        if ip_address not in salt_map: # If no salt for the IP
            salt_map[ip_address] = random_string() # Add a new salt for the IP
        random_salt = salt_map[ip_address]
        hashwithsalt = sha1_value(ip_address + random_salt)
        # We only want unique ID readable ID
        userdata_json[key]['ip'] = hashwithsalt[0:10] # Take 10 first chars
    for key, value in userdata_json.items():
        print(key, value)

if __name__ == '__main__':
    main()
