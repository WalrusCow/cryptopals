import random
import urllib.parse

import aes
import cryptUtil
import pkcs
import byteECB

def encode(kvpList):
    # Do dumb quoting because proper urllib encoding will screw up due to
    # "admin" being padded with \x0b which is encoded differently and thus
    # not pkcs stripped properly
    quote = lambda x: x.replace('&', '%26').replace('=', '%3D')
    s = '&'.join(quote(k) + '=' + quote(v) for k, v in kvpList)
    # bytes forever
    return s.encode()

def decode(qs):
    if type(qs) == bytes: qs = qs.decode()
    return dict(urllib.parse.parse_qsl(qs))

class ProfileCipher():
    ''' Encrypt/decrypt profiles according to a constant cipher. '''
    def __init__(self):
        self._cipher = aes.ecb(cryptUtil.randomBytes(16))

    def _profile_for(self, email):
        if type(email) == bytes: email = email.decode()
        return encode([('email', email), ('uid', '10'), ('role', 'user')])

    def encrypt(self, email):
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
    Find kind of padding used.
        - Use email of "XXXXXXX" as length requires
    Use email to create a block that is adminPPPPPPPPPPP where `P` are the
    bytes that the encryptor uses. This is block 2.
        - Use email "adminPPPPPPPPPPP@email.com"
    Now take some email (of length used to generate block 1) and replace
    the last block to be block 2.  Now block 1 and block 2 will be adjacent
    and will say XXXXuid=10&role=adminPPPPPPPPPPPPP
'''

def makeAdmin(cipher):
    blockSize, _ = byteECB.findBlockSize(cipher.encrypt)

    # TODO: Determine programmatically where in the data our string
    # is inserted, and then find the length of the prefix of it.
    adminPad = blockSize - len(b'email=')

    # TODO: Programmatically, strip the prefix foud from ^ and determine the
    # secret text like in byteECB.  Then find where "role=user" is located
    # and get this proper pad
    rolePad =  adminPad + (blockSize - len('&uid=10&role='))
    text = cipher.encrypt(b'x' * rolePad)

    # TODO: Find this block number programmatically
    roleBlock = cryptUtil.getNthBlock(text, blockSize, 1)

    # TODO: Detect PKCS #7 padding (or other padding kind)
    # We will assuming pkcs #7 padding, but we can easily find out
    # if this is the case, and adjust our padding appropriately
    text = cipher.encrypt(b'x' * adminPad + pkcs.pad(b'admin', blockSize))
    adminBlock = cryptUtil.getNthBlock(text, blockSize, 1)

    text = cipher.encrypt('x' * rolePad)
    myText =  cryptUtil.getNthBlock(text, blockSize, 0) + roleBlock + adminBlock
    try:
        if cipher.decrypt(myText)['role'] == 'admin':
            return True
    except:
        pass
    return False

if __name__ == '__main__':
    print('Success' if makeAdmin(ProfileCipher()) else 'Failure')
    #print(encode({'email': 'fo@b.com&x=y', 'uid': 10, 'role': 'user'}))
    #print(decode('foo=bar&baz=qux&zap=zazzle'))
