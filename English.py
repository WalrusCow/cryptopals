# Module for identifying English text
# Author: William McDonald
# Date: July 11, 2014

from collections import Counter
from math import sqrt

# Frequency of English letters, including space
from _EnglishFrequency import *

def _countChars(byteArray):
    def isWhitespace(byte):
        return any(byte == ord(c) for c in '\n\r\t ')

    def getChar(byte):
        return ' ' if isWhitespace(byte) else chr(byte)

    return Counter(getChar(b) for b in byteArray.lower())


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

    # Some very unlikely characters
    unlikely = ''.join(k for k, v in charFrequency.items() if v < 0.0001)
    s = sum(freq[ch] for ch in unlikely)
    # If we are any greater than quit
    if s > 1.5 * sum(charFrequency[ch] for ch in unlikely):
        return False

    return distance(freq) < maxDistance
