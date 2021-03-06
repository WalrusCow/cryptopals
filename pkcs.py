def pad(byteArray, blockSize):
    ''' Pad bytes fit in given block size. '''
    pad = blockSize - (len(byteArray) % blockSize)
    return byteArray + bytes(pad for _ in range(pad))

def getPadding(byteArray):
    if not byteArray: return None
    b = byteArray[-1]
    l = len(byteArray)
    # Last `b` bytes are all the same
    return b if all(x == b for x in byteArray[l-b:]) else None

def strip(byteArray):
    ''' Strip pkcs padding, or throw if invalid padding. '''
    b = getPadding(byteArray)
    if b is None:
        raise ValueError('Bytes have invalid padding')
    l = len(byteArray)
    return byteArray[:l-b]


if __name__ == '__main__':
    print(pad(b'YELLOW SUBMARINE', 20))
    print(pad(b'YELLOW SUBMARINE', 16))
    print(strip(pad(b'YELLOW SUBMARINE', 20)))
    print(strip(pad(b'YELLOW SUBMARINE', 16)))
