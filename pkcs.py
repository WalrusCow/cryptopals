def pad(byteArray, blockSize):
    ''' Pad bytes fit in given block size. '''
    pad = blockSize - (len(byteArray) % blockSize)
    return byteArray + bytes(pad for _ in range(pad))

if __name__ == '__main__':
    print(pad(b'YELLOW SUBMARINE', 20))
