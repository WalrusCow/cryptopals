#!/usr/bin/python3

from singleChar import decryptSingleCharXor

def solve(encryptedStrings):
    ''' Find the string that has been encrypted with a single character
    XOR cipher in the iterable of strings. Input is hex encoded. '''
    for string in encryptedStrings:
        d = decryptSingleCharXor(bytes.fromhex(string))
        if not d: continue
        print('Line:\n{}\nDecrypted:\nKey: {} Text: {}'.format(string, *d))

if __name__ == '__main__':
    with open('maybestrings.txt') as f:
        # Remove trailing newline from file iteration
        solve(map(str.strip, f))
