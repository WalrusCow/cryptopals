#!/usr/bin/python3
import base64
import itertools
import operator

import English
import Hamming
import singleByte

def _getKeysizeDistances(byteArray, *, keyMin=2, keyMax=50, samples=2):
    ''' Get normalized Hamming distances between first and second byte groups.
    of likely key lengths. '''

    distances = dict()
    for size in range(keyMin, keyMax):
        d = 0
        # Avoid over sampling
        for i in range(min(samples, size // 2)):
            b1 = byteArray[size*i*2:size*(i*2 + 1)]
            b2 = byteArray[size*(i*2 + 1):size*2*(i + 1)]
            d += Hamming.distance(b1, b2) / size
        distances[size] = d / samples

    return distances


def _transposeBytes(byteArray, size):
    ''' Return generator of generators for byte blocks. '''
    for i in range(0, size):
        # Generators for all elements with index of 0 mod i
        yield bytes(itertools.islice(byteArray, i, None, size))


def _orderByLikelyKeysize(distances):
    ''' Take a dictionary of distances, return a generator of keysizes
    ordered from most to least likely. '''
    distances = sorted(distances.items(), key=operator.itemgetter(1))
    return list(map(operator.itemgetter(0), distances))


def decrypt(byteArray):
    ''' Break English ciphertext encoded with repeating key xor. '''
    distances = _getKeysizeDistances(byteArray)
    keysizes = _orderByLikelyKeysize(distances)

    for size in keysizes[:10]:
        keys = []
        texts = []

        # Now let us create magical generators
        for byteBlock in _transposeBytes(byteArray, size):
            ans = singleByte.decrypt(byteBlock)
            if ans is None:
                break
            key, text = ans
            keys.append(key)
            texts.append(text)
        else:
            return bytes(keys), bytes(xor(byteArray, itertools.cycle(keys)))


def xor(byteArray, keyGen):
    ''' For each byte of the array, get a byte from the key generator.
    Then xor against the key generator.
    Make the keyGen input like so: itertools.cycle(b'#yolo')
    '''
    for byte, key in zip(byteArray, keyGen):
        yield byte ^ key


if __name__ == '__main__':
    with open('texts/repeatingkey.txt', 'rb') as f:
        byteArray = base64.b64decode(f.read())
        ans = decrypt(byteArray)
        if ans is None:
            print('No valid decryption found.')
        else:
            key, text = ans
            print('Key: {}\nText:{}'.format(key.decode(), text.decode()))
