'''
Problem 10
'''

from random import randint

import aes
import pkcs

def _randomBytes(n):
    return bytes(randint(0, 255) for _ in range(n))

def encryptionOracle(text):
    # Some random padding
    frontPad = randint(5, 10)
    endPad = randint(5, 10)
    text = _randomBytes(frontPad) + text + _randomBytes(endPad)

    # Now pad text to block size with pkcs
    text = pkcs.pad(text, 16)

    key = _randomBytes(16)
    if randint(0, 1):
        iv = _randomBytes(16)
        cipher = aes.cbc(key, iv)
        method = 'CBC'
    else:
        cipher = aes.ecb(key)
        method = 'ECB'
    return cipher.encrypt(text), method

def getMethod(text):
    ''' Determine if text was encrypted CBC or ECB. '''
    b2 = text[16:32]
    b3 = text[32:48]
    return 'ECB' if b2 == b3 else 'CBC'

if __name__ == '__main__':
    text = b'x' * (16 * 3)
    for _ in range(30):
        cipherText, method = encryptionOracle(text)
        print(getMethod(cipherText) == method)
