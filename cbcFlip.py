import aes
import pkcs
from cryptUtil import randomBytes, blockSize, getNthBlock

class Quoter():
    replaceList = [(b';', b'%3B'), (b' ', b'%20'), (b'=', b'%3D')]

    @staticmethod
    def _multiReplace(replaceList):
        def replace(text):
            for r in replaceList: text = text.replace(*r)
            return text
        return replace

    @staticmethod
    def quote(text):
        return Quoter._multiReplace(Quoter.replaceList)(text)

    @staticmethod
    def unquote(text):
        return Quoter._multiReplace((v, k) for k, v in Quoter.replaceList)(text)

    @staticmethod
    def parse(text):
        pairs = (pair.split(b'=', 1) for pair in text.split(b';') if b'=' in pair)
        return [(Quoter.unquote(k), Quoter.unquote(v)) for k, v in pairs]

class Encryptor():
    def __init__(self):
        self._prefix = b'comment1=cooking%20MCs;userdata='
        self._suffix = b';comment2=%20like%20a%20pound%20of%20bacon'
        self._cipher = aes.cbc(randomBytes(16), randomBytes(16))

    def encrypt(self, text):
        if type(text) == str: text = text.encode()
        text = self._prefix + Quoter.quote(text) + self._suffix
        return self._cipher.encrypt(pkcs.pad(text, 16))

    def decrypt(self, text):
        if type(text) == str: text = text.encode()
        return pkcs.strip(self._cipher.decrypt(text))

def makeAdmin(encrypt):
    ''' Return ciphertext that has role=admin when decrypted. '''
    def xor(b1, b2):
        return bytes(x ^ y for x, y in zip(b1, b2))

    bs = blockSize(encrypt)
    # it's cool that the prefix is known to be 32 bytes == 2 blocks lol
    # otherwise we'd have to get the prefix length which might be ugly
    data = b'x'
    original = encrypt(data * 2 * bs)
    oldBlock = getNthBlock(original, bs, 2)
    # This is one block long ^_^
    payload = b';role=admin;foo='

    # Flip every bit in the original block where payload and data differ
    newBlock = xor(oldBlock, xor(payload, data * len(payload)))
    return original[:2 * bs] + newBlock + original[2 * bs + len(newBlock):]

def isAdmin(kvpList):
    return (b'role', b'admin') in kvpList

if __name__ == '__main__':
    e = Encryptor()
    text = makeAdmin(e.encrypt)
    kvpList = Quoter.parse(e.decrypt(text))
    print('Success' if isAdmin(kvpList) else 'Failure')
