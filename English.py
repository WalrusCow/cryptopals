# Module for identifying English text
# Author: William McDonald
# Date: July 11, 2014

from collections import Counter
from math import sqrt

# Frequency of English letters, including space
from _EnglishFrequency import *

def _countChars(byteArray):
    def lowercase(byte):
        return byte + ord('a') - ord('A')

    def isWhitespace(byte):
        return any(byte == ord(c) for c in '\n\r\t ')

    def gen():
        for b in byteArray:
            if ord('A') <= b <= ord('Z'):
                yield chr(lowercase(b))
            elif isWhitespace(b):
                yield ' '
            else:
                yield chr(b)

    return Counter(gen())


def _printable(b):
    GOOD_WHITESPACE = '\n\r\t'
    if any(b == ord(c) for c in GOOD_WHITESPACE):
        return True
    return 32 <= b <= 126


def _norm(v):
    return sqrt(sum(x * x for x in v))


def _charFreq(byteArray):
    count = _countChars(byteArray)
    for k, v in count.items():
        count[k] /= len(byteArray)
    return count


def distance(freq):
    ''' Return the vector distance between the given letter frequency
    and the average frequency of letters in English. '''
    if not isinstance(freq, dict):
        freq = _charFreq(freq)
    return _norm(v - charFrequency[k] for k, v in freq.items())


def probable(byteArray, *, maxDistance=0.18):
    ''' Return true if the array of bytes is "probably" English. '''
    if not all(_printable(b) for b in byteArray):
        # Contains non-printable bytes: cannot be English
        return False

    freq = _charFreq(byteArray)
    return distance(freq) < maxDistance
