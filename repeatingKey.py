#!/usr/bin/python3
import base64

import hamming

def _makeKeyGen(byteArray):
    ''' Create an infinite circular generator of the bytes. '''
    while True:
        yield from byteArray


def decrypt(byteArray):
    ''' Break English ciphertext encoded with repeating key xor. '''


def xor(byteArray, keyGen):
    ''' For each byte of the array, get a byte from the key generator.
    Then xor against the key generator. '''
    for byte, key in zip(byteArray, keyGen):
        yield byte ^ key


if __name__ == '__main__':
    # Convert everything to bytes!
    with open('repeatingkey.txt') as f:
        ctext = ''.join(map(str.strip, f)).encode()
        ctext = base64.b64decode(ctext)
    plainText = ("Burning 'em, if you ain't quick and nimble\n"
                 "I go crazy when I hear a cymbal").encode()
    ans = ('0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a2622632'
           '4272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b202831'
           '65286326302e27282f')
    ans = bytes.fromhex(ans)

    encrypted = bytes(xor(plainText, _makeKeyGen('ICE'.encode())))
    print(encrypted == ans)
