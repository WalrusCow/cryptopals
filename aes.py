import base64

from Crypto.Cipher import AES

import cryptUtil

class ecb:
    def __init__(self, key):
        self._cipher = AES.new(key)
    def encrypt(self, text):
        return self._cipher.encrypt(text)
    def decrypt(self, text):
        return self._cipher.decrypt(text)

class cbc:
    def __init__(self, key, iv):
        if len(key) != len(iv):
            raise ValueError('IV and key must be same length')

        self._key = bytes(key)
        self._iv = bytes(iv)
        self._ecb = ecb(key)
        self._blockSize = len(key)

    def _textCheck(func):
        def wrapper(self, text, *args, **kwargs):
            ''' Force text to bytes; check text length. '''
            if len(text) % self._blockSize:
                raise ValueError('Plaintext length not a multiple of key length')
            return func(self, bytes(text), *args, **kwargs)
        return wrapper

    @staticmethod
    def _xor(b1, b2):
        return bytes(x ^ y for x, y in zip(b1, b2))

    @_textCheck
    def encrypt(self, text):
        ''' cbc encrypt text. throw ValueError if wrong block size. '''
        cipherText = b''
        last = self._iv
        for block in cryptUtil.blockIter(text, self._blockSize):
            last = self._ecb.encrypt(self._xor(block, last))
            cipherText += last
        return cipherText

    @_textCheck
    def decrypt(self, text):
        ''' throw ValueError if wrong block size. '''
        plainText = b''
        last = self._iv
        for block in cryptUtil.blockIter(text, self._blockSize):
            plainText += self._xor(self._ecb.decrypt(block), last)
            last = block
        return plainText

if __name__ == '__main__':
    key = b'YELLOW SUBMARINE'
    #ecbCipher = ecb(key)
    #with open('texts/ecb.txt') as f:
    #    text = ''.join(f.read().strip()).encode()
    #    text = base64.b64decode(text)
    #    print(ecbCipher.decrypt(text))
    cbcCipher = cbc(key, bytes(16))
    with open('texts/cbc_decrypt.txt') as f:
        text = ''.join(f.read().strip()).encode()
        text = base64.b64decode(text)
        print(cbcCipher.decrypt(text))
