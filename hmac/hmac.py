'''
HMAC scheme consists of an inner and outer hash.

MD5 example from RFC 2104.

https://datatracker.ietf.org/doc/html/rfc2104

HMACk(x) = h[ (k+ XOR opad) || h[(k+ XORed ipad) || x] ]
'''
from hashlib import md5

def hmac_md5(key, text):
    '''
    hmac_md5(key="Jefe", text="what do ya want for nothing?")

    key =         "Jefe"
    data =        "what do ya want for nothing?"
    data_len =    28 bytes
    digest =      0x750c783e6ab0b503eaa86e310a5db738

    returns 750c783e6ab0b503eaa86e310a5db738
    '''
    B = 64 # Block byte length
    ipad = b'\x36' * B # ipad = the byte 0x36 repeated B times
    opad = b'\x5c' * B # opad = the byte 0x5C repeated B times
    # 1. Append zeros to the end of the key to create a B=64 byte string
    key_bytes = key.encode().ljust(B, b'\0')
    # 2. XOR (bitwise exclusive-OR) the B=64 byte string computed in step (1) with ipad
    bitwise_ipad_bytes = bytes([a ^ b for (a, b) in zip(ipad, key_bytes)])
    # 3. Append the stream of data 'text' to the B=64 byte string resulting from step (2)
    inner_data = bitwise_ipad_bytes + text.encode()
    # 4. Apply hashing to the stream generated in step (3)
    inner_hash = md5(inner_data).digest()
    # 5. XOR (bitwise exclusive-OR) the B=64 byte string computed in step (1) with opad
    bitwise_opad_bytes = bytes([a ^ b for (a, b) in zip(opad, key_bytes)])
    # 6. Append the hashing result from step (4) to the B=64 byte string resulting from step (5)
    outer_data = bitwise_opad_bytes + inner_hash
    # 7. Apply hashing to the stream generated in step (6) and output the result
    outer_hash = md5(outer_data).digest()
    # Finally, return the hex value of the HMAC hash
    return outer_hash.hex()

def main():
    ''' Testing HMAC '''
    # Use the example from the RFC 2104
    message = "what do ya want for nothing?"
    key = "Jefe"
    print('Message: ' + message)
    print('Secret shared key: ' + key)
    # Calculate the hmac md5 value
    hmac_value = hmac_md5(key, message)
    print('HMAC: ' + hmac_value)
    # Test that the function returns the correct value
    expected_result = '750c783e6ab0b503eaa86e310a5db738'
    assert hmac_value == expected_result

if __name__ == '__main__':
    main()
