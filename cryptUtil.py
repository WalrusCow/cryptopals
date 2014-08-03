from random import randint

def blockIter(lst, blockSize):
    ''' Iterate over list in chunk of size blockSize. '''
    start = 0
    while start < len(lst):
        yield lst[start:start + blockSize]
        start += blockSize

def randomBytes(n):
    return bytes(randint(0, 255) for _ in range(n))

def getNthBlock(text, blockSize, n):
    ''' Zero indexed. '''
    return text[blockSize * n : blockSize * (n+1)]

def hexify(b):
    ''' Print bytes as hex, colon separated. '''
    return ":".join("{:02x}".format(byte) for byte in b)
