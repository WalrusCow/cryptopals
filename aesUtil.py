import aes
import pkcs
from cryptUtil import blockIter, getNthBlock

def blockSize(encrypt):
    ''' Take in an encryption function and return the block size. '''
    text = b'\x00'
    l = len(encrypt(text))
    # Say max block size is 128 (arbitrarily chosen)
    for _ in range(128):
        text += b'\x00'
        n = len(encrypt(text))
        if n != l:
            return n - l
    # No block size found
    return None

def method(encrypt, blockSize):
    ''' Determine if text was encrypted CBC or ECB. '''
    text = encrypt(bytes(blockSize * 3))
    b1 = getNthBlock(text, blockSize, 0)
    b2 = getNthBlock(text, blockSize, 1)
    return 'ECB' if b1 == b2 else 'CBC'

def prefixLength(encrypt, bs):
    ''' Find the length of a prefix prepended to input text. '''
    baseText = encrypt(b'')
    # Find the first block that changes
    inputText = b'\x00'
    t = encrypt(inputText)
    idx = None
    while idx is None:
        gen = enumerate(zip(blockIter(baseText, bs), blockIter(t, bs)))
        for idx, (baseBlock, newBlock) in gen:
            if baseBlock != newBlock: break
        else:
            # Increment the input text - in case there are many blocks
            # of all `0` or something
            inputText += b'\x00'
            t = encrypt(inputText)
            idx = None

    # This is the block of all '\x00' following the last prefix block
    newBlock = getNthBlock(encrypt(bytes(bs * 2)), bs, idx + 1)
    for l in range(bs * 2, 0, -1):
        block = getNthBlock(encrypt(bytes(l)), bs, idx + 1)
        if block != newBlock:
            # We want the length that is the first time the block changes
            break
    return idx * bs + (2 * bs - (l + 1))

def suffix(encrypt, blockSize, prefixLength):
    ''' Find the suffix appended to input text. '''
    prefixOverflow = blockSize - (prefixLength % blockSize)
    def iterBytes():
        # Printable first ...
        for b in range(32, 128): yield bytes([b])
        for b in range(0, 32): yield bytes([b])
        for b in range(128, 256): yield bytes([b])

    def findNextByte(known):
        inputLen = blockSize - (len(known) % blockSize) - 1
        inputLen = (inputLen - prefixLength) % blockSize
        blockNum = (prefixLength + inputLen + len(known)) // blockSize
        text = bytes(inputLen)

        # This is the encrypted block with unknown byte as the last byte
        short = getNthBlock(encrypt(text), blockSize, blockNum)

        # From now on we want to use the prefix, known and random byte
        # to push our guessed byte to the end of a block
        text += known
        for b in iterBytes():
            if short == getNthBlock(encrypt(text + b), blockSize, blockNum):
                return b

    unknownLength = 0
    baseLength = len(encrypt(b''))
    for l in range(1, blockSize + 1):
        if len(encrypt(bytes(l))) != baseLength:
            unknownLength = baseLength - l
            break
    unknownLength -= prefixLength
    known = b''
    for knownLength in range(unknownLength):
        known += findNextByte(known)
    return known

if __name__ == '__main__':
    from cryptUtil import randomBytes, hexify
    from random import randint
    class _Encryptor():
        def __init__(self, suffix):
            self.prefix = randomBytes(randint(1, 600))
            self._cipher = aes.ecb(b'YELLOW SUBMARINE')
            self.secret = suffix

        def encrypt(self, text):
            text = self.prefix + text + self.secret
            return self._cipher.encrypt(pkcs.pad(text, 16))

    secrets = [b'short', b'long - that is longer than one block at least :)']
    for secret in secrets:
        e = _Encryptor(secret)
        bs = blockSize(e.encrypt)
        pl = prefixLength(e.encrypt, bs)
        s = suffix(e.encrypt, bs, pl)
        print('Fail' if s != secret else 'Success')
