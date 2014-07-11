#!/usr/bin/python3

import random
from collections import defaultdict
from math import sqrt

def countChars(byteArray):
    def lowercase(byte):
        return b + ord('a') - ord('A')

    d = defaultdict(int)
    for b in byteArray:
        if ord('A') <= b <= ord('Z'): d[chr(lowercase(b))] += 1
        elif ord('a') <= b <= ord('z'): d[chr(b)] += 1
        elif ord(' ') == b: d[chr(b)] += 1
        else: d['nonchar'] += 1
    return d

def isPrintable(b):
    GOOD_WHITESPACE = '\n\r\t'
    if any(b == ord(c) for c in GOOD_WHITESPACE):
        return True
    return 32 <= b <= 126

def norm(v):
    return sqrt(sum(x * x for x in v))

def englishDistance(byteArray):
    MAX_NONCHAR = 0.05

    # Frequency of English letters, counting space
    engFreq = {' ': 0.1831685753, 'a': 0.0655307059, 'b': 0.0127076566,
               'c': 0.0226508836, 'd': 0.0335227377, 'e': 0.1021787708,
               'f': 0.0197180888, 'g': 0.0163586607, 'h': 0.0486220925,
               'i': 0.0573425524, 'j': 0.0011440544, 'k': 0.0056916712,
               'l': 0.0335616550, 'm': 0.0201727037, 'n': 0.0570308374,
               'o': 0.0620055405, 'p': 0.0150311560, 'q': 0.0008809302,
               'r': 0.0497199926, 's': 0.0532626738, 't': 0.0750999398,
               'u': 0.0229520040, 'v': 0.0078804815, 'w': 0.0168961396,
               'x': 0.0014980832, 'y': 0.0146995463, 'z': 0.0005979301}

    if not all(isPrintable(b) for b in byteArray):
        # Contains non-printable bytes
        return float("inf")

    d = countChars(byteArray)

    # Simple extra check for non a-z or ' ' chars
    if d['nonchar'] / len(byteArray) >= MAX_NONCHAR:
        return float("inf")
    del d['nonchar']

    for k, v in d.items():
        d[k] /= len(byteArray)
        # Compute distance between frequencies
        d[k] = abs(d[k] - engFreq[k])

    # Check "vector" distance
    return norm(d.values())

def xorSingleChar(byteArray, i):
    ''' xor bytes against int (generator) '''
    for b in byteArray:
        yield b ^ i

def isProbableEnglish(byteArray):
    MAX_DISTANCE = 0.15
    return englishDistance(byteArray) < MAX_DISTANCE

def decryptSingleCharXor(byteArray):
    ''' Decrypt a single byte xor cipher. '''

    # Iterate over all possible byte values
    for i in range(0, 256):
        decrypt = bytes(xorSingleChar(byteArray, i))
        #dist = englishDistance(s)
        if isProbableEnglish(decrypt):
            return chr(i), decrypt

    # No valid one found. Here we can get the max if we wanted
    return None

if __name__ == '__main__':
    # Matasano string
    b = bytes.fromhex('1b37373331363f78151b7f2b783431333d'
                      '78397828372d363c78373e783a393b3736')

    # Some random short samples from wikipedia
    sentences = [
        b"Paul was not a religious man",
        b"With their intended targets being other",
        b"and they labelled themselves 'the realest guys in the room'",
        b"when negotiations for a new three-year collective bargaining",
        b"under pressures of up to 4 times normal air",
        # Decrypt the Matasano string, since we know the answer
        xorSingleChar(b, ord('X')),
    ]

    for s in sentences:
        encrypted = bytes(xorSingleChar(s, random.randint(32, 127)))
        ans = decryptSingleCharXor(encrypted)
        if ans is None:
            print('No valid decryption')
        else:
            print('Key {} decodes to: {}'.format(*ans))
