def _blockIter(lst, blockSize):
    ''' Iterate over list in chunk of size blockSize. '''
    start = 0
    while start < len(lst):
        yield lst[start:start + blockSize]
        start += blockSize


def isECB(byteArray):
    ''' Try to determine if an array of bytes is ECB encoded. '''
    # We know that the same 16 bytes will encode to the same thing
    # What if we look for multiple 16 byte objects

    # Iterate over 16 byte blocks
    s = frozenset(_blockIter(byteArray, 16))
    return len(s) != (len(byteArray) / 16)






def findECB(byteArrays):
    ''' Find the ECB hex in an array of bytes. '''
    for i, arr in enumerate(byteArrays):
        if isECB(arr):
            print('Found ECB at {}'.format(i))


if __name__ == '__main__':
    with open('ecb_detect.txt') as f:
        # Create a list of bytes from the lines of the file
        # Each line is hex encoded, and will end with a newline so we strip
        hexes = list(map(bytes.fromhex, map(str.strip, f)))
        findECB(hexes)
