#!/usr/bin/python3

import base64

def xorBytes(b1, b2):
    ''' Return bytes that are xor of b1, b2. '''
    n1 = int.from_bytes(b1, 'little')
    n2 = int.from_bytes(b2, 'little')
    return (n1 ^ n2).to_bytes(max(len(b1), len(b2)), 'little')


# Yay for inputs
s1 = bytes.fromhex('1c0111001f010100061a024b53535009181c')
s2 = bytes.fromhex('686974207468652062756c6c277320657965')

s3 = '746865206b696420646f6e277420706c6179'.upper().encode()
print(base64.b16encode(xorBytes(s1, s2)) == s3)
