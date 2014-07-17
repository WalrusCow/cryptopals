#!/usr/bin/python3

import random

import English

def xor(byteArray, i):
    ''' xor bytes against int (generator) '''
    for b in byteArray:
        yield b ^ i


def decrypt(byteArray):
    ''' Decrypt a single byte xor cipher. '''

    minD = float('inf')
    best = (-1, b'')

    # Iterate over all possible byte values
    for i in range(0, 256):
        decrypt = bytes(xor(byteArray, i))
        if English.probable(decrypt):
            return i, decrypt
        else:
            d = English.distance(decrypt)
            if d < minD:
                best = (i, decrypt)
                minD = d

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
        xor(b, ord('X')),
    ]

    for s in sentences:
        encrypted = bytes(xor(s, random.randint(32, 127)))
        ans = decrypt(encrypted)
        if ans is None:
            print('No valid decryption')
        else:
            print('Key {} decodes to: {}'.format(*ans))
