import random
import urllib.parse

import aes
import cryptUtil
import pkcs
import aesUtil

def encode(kvpList):
    # Do dumb quoting because proper urllib encoding will screw up due to
    # "admin" being padded with \x0b which is encoded differently and thus
    # not pkcs stripped properly
    def byteify(x): return x.encode() if type(x) == str else x
    kvpList = ((byteify(k), byteify(v)) for k, v in kvpList)
    quote = lambda x: x.replace(b'&', b'%26').replace(b'=', b'%3D')
    return b'&'.join(quote(k) + b'=' + quote(v) for k, v in kvpList)

def decode(qs):
    if type(qs) == bytes: qs = qs.decode()
    return dict(urllib.parse.parse_qsl(qs))

class ProfileCipher():
    ''' Encrypt/decrypt profiles according to a constant cipher. '''
    def __init__(self):
        self._cipher = aes.ecb(cryptUtil.randomBytes(16))

    def _profile_for(self, email):
        return encode([('email', email), ('uid', '10'), ('role', 'user')])

    def encrypt(self, email):
        if type(email) == str: email = email.encode()
        text = pkcs.pad(self._profile_for(email), 16)
        return self._cipher.encrypt(text)

    def decrypt(self, text):
        return decode(pkcs.strip(self._cipher.decrypt(text)))

'''
Assumptions:
    (1) Consistent ordering of KVP
    (2) Email is first
    (3) uid constant
Idea:
    Use email to create a block that is XXXXuid=10&role=  This is block 1.
    Find kind of padding used (we assume pkcs7).
        - Use email of "XXXXXXX" as length requires
    Use email to create a block that is adminPPPPPPPPPPP where `P` are the
    bytes that the encryptor uses. This is block 2.
        - Use email "adminPPPPPPPPPPP@email.com"
    Now take some email (of length used to generate block 1) and replace
    the last block to be block 2.  Now block 1 and block 2 will be adjacent
    and will say XXXXuid=10&role=adminPPPPPPPPPPPPP
'''

def makeAdmin(cipher):
    # Shorthand
    encrypt = cipher.encrypt
    blockSize = aesUtil.blockSize(encrypt)

    prefixLen = aesUtil.prefixLength(encrypt, blockSize)
    adminPad = blockSize - (prefixLen % blockSize)

    rolePad = adminPad + (blockSize - len('&uid=10&role='))
    text = encrypt(b'x' * rolePad)

    roleBlock = cryptUtil.getNthBlock(text, blockSize, 1)

    text = encrypt(b'x' * adminPad + pkcs.pad(b'admin', blockSize))
    adminBlock = cryptUtil.getNthBlock(text, blockSize, 1)

    text = encrypt(b'x' * rolePad)
    myText =  cryptUtil.getNthBlock(text, blockSize, 0) + roleBlock + adminBlock
    try:
        return cipher.decrypt(myText)['role'] == 'admin':
    except:
        return False

if __name__ == '__main__':
    print('Success' if makeAdmin(ProfileCipher()) else 'Failure')
