def weight(byte):
    ''' Compute the Hamming weight of a byte. '''
    w = 0
    while byte:
        w += 1
        byte &= byte - 1

def distance(b1, b2):
    ''' Compute the Hamming distance between the two byte arrays. '''
    # Sum Hamming weight of xor of bytes
    d = sum(weight(x ^ y) for x, y in zip(b1, b2))
    # Add the number of extra bits if any. Usually lengths are equal
    return d + abs(len(b1) - len(b2)) * 8
