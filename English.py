# Module for identifying English text
# Author: William McDonald
# Date: July 11, 2014

from collections import defaultdict
from math import sqrt

# Frequency of English letters, including space
_freq = {' ': 0.1831685753, 'a': 0.0655307059, 'b': 0.0127076566,
         'c': 0.0226508836, 'd': 0.0335227377, 'e': 0.1021787708,
         'f': 0.0197180888, 'g': 0.0163586607, 'h': 0.0486220925,
         'i': 0.0573425524, 'j': 0.0011440544, 'k': 0.0056916712,
         'l': 0.0335616550, 'm': 0.0201727037, 'n': 0.0570308374,
         'o': 0.0620055405, 'p': 0.0150311560, 'q': 0.0008809302,
         'r': 0.0497199926, 's': 0.0532626738, 't': 0.0750999398,
         'u': 0.0229520040, 'v': 0.0078804815, 'w': 0.0168961396,
         'x': 0.0014980832, 'y': 0.0146995463, 'z': 0.0005979301}

def _countChars(byteArray):
    def lowercase(byte):
        return b + ord('a') - ord('A')

    d = defaultdict(int)
    for b in byteArray:
        if ord('A') <= b <= ord('Z'): d[chr(lowercase(b))] += 1
        elif ord('a') <= b <= ord('z'): d[chr(b)] += 1
        elif ord(' ') == b: d[chr(b)] += 1
        else: d['nonletter'] += 1
    return d


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
    return _norm(v - _freq[k] for k, v in freq.items())


def probable(byteArray):
    ''' Return true if the array of bytes is "probably" English. '''
    if not all(_printable(b) for b in byteArray):
        # Contains non-printable bytes: cannot be English
        return False

    # Maximum percentage of non-letter (or space) characters
    MAX_NON_LETTER = 0.05
    # Maximum frequency distance
    MAX_DISTANCE = 0.15

    freq = _charFreq(byteArray)
    if freq['nonletter'] > MAX_NON_LETTER:
        return False
    del freq['nonletter']

    return distance(freq) < MAX_DISTANCE
