import base64

import aes
import cryptUtil
import pkcs
import ecbUtil

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

def findSecret(cipher):
    ''' Find the secret message hidden by encrypt. '''
    blockSize = cryptUtil.blockSize(cipher.encrypt)
    if ecbUtil.method(cipher.encrypt, blockSize) != 'ECB':
        return
    prefixLength = ecbUtil.prefixLength(cipher.encrypt, blockSize)
    return ecbUtil.suffix(cipher.encrypt, blockSize, prefixLength)

if __name__ == '__main__':
    print(findSecret(SekritCipher()))
