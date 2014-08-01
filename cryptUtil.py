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
    return text[blockSize * n : blockSize * (n+1)]

