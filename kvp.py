import urllib.parse

import aes
import cryptUtil
import pkcs
import ecbUtil

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

def makeAdmin(cipher):
    # Shorthand
    encrypt = cipher.encrypt
    blockSize = cryptUtil.blockSize(encrypt)

    prefixLen = ecbUtil.prefixLength(encrypt, blockSize)
    adminPad = blockSize - (prefixLen % blockSize)
    rolePad = adminPad + (blockSize - len('&uid=10&role='))

    text = encrypt(b'x' * rolePad)
    roleBlock = cryptUtil.getNthBlock(text, blockSize, 1)

    text = encrypt(b'x' * adminPad + pkcs.pad(b'admin', blockSize))
    adminBlock = cryptUtil.getNthBlock(text, blockSize, 1)

    text = encrypt(b'x' * rolePad)
    myText = cryptUtil.getNthBlock(text, blockSize, 0) + roleBlock + adminBlock
    try:
        return cipher.decrypt(myText)['role'] == 'admin'
    except:
        return False

if __name__ == '__main__':
    print('Success' if makeAdmin(ProfileCipher()) else 'Failure')
