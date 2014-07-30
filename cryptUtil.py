def blockIter(lst, blockSize):
    ''' Iterate over list in chunk of size blockSize. '''
    start = 0
    while start < len(lst):
        yield lst[start:start + blockSize]
        start += blockSize

