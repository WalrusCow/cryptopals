import base64
from random import randint

import aes
import cryptUtil
import pkcs

def _iterBytes():
    ''' An interator for the possible values of a byte, in a smart order. '''
    # Printable first ...
    yield from range(32, 128)
    yield from range(0, 32)
    yield from range(128, 256)

class SekritCipher:
    def __init__(self):
        self._cipher = aes.ecb(cryptUtil.randomBytes(16))

    def encrypt(self, text):
        sekrit = ('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg'
                  'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq'
                  'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg'
                  'YnkK')
        text += base64.b64decode(sekrit.encode())
        text = pkcs.pad(text, 16)
        return self._cipher.encrypt(text)

def findBlockSize(encrypt):
    ''' Find block size used in `encrypt`. '''
    text = b'x'
    l = len(encrypt(text))
    # Say max block size is 128
    for _ in range(128):
        text += b'x'
        n = len(encrypt(text))
        if n != l:
            return n - l, l - len(text)

def findMethod(encrypt, blockSize):
    ''' Determine if text was encrypted CBC or ECB. '''
    text = encrypt(b'x' * (blockSize * 3))
    b1 = cryptUtil.getNthBlock(text, blockSize, 0)
    b2 = cryptUtil.getNthBlock(text, blockSize, 1)
    return 'ECB' if b1 == b2 else 'CBC'

def findNextByte(encrypt, blockSize, known):
    ''' Find next byte given starting text. '''
    # Length of prefix we need to push the next unknown byte to be the last
    # byte in a block
    prefixLen = blockSize - (len(known) % blockSize) - 1
    blockNum = (prefixLen + len(known)) // blockSize
    prefix = bytes(prefixLen)

    # This is the encrypted block containing the unknown byte as the last byte
    short = cryptUtil.getNthBlock(encrypt(prefix), blockSize, blockNum)

    # From now on we want to use the prefix, known and random byte
    # to push our guessed byte to the end of a block
    prefix += known
    for b in _iterBytes():
        byte = bytes([b])
        if short == cryptUtil.getNthBlock(encrypt(prefix + byte),
                                          blockSize,
                                          blockNum):
            return byte

def findSecret(cipher):
    ''' Find the secret message hidden by encrypt. '''
    blockSize, unknownLength = findBlockSize(cipher.encrypt)
    if findMethod(cipher.encrypt, blockSize) != 'ECB':
        return
    known = b''
    for knownLength in range(unknownLength - 1):
        # Prefix to find next byte with
        known += findNextByte(cipher.encrypt, blockSize, known)
    return known

if __name__ == '__main__':
    print(findSecret(SekritCipher()))
