import base64

def xorBytes(b1, b2):
    ''' Return bytes that are xor of b1, b2. '''
    return bytes(x ^ y for x, y in zip(b1, b2))


if __name__ == '__main__':
    s1 = bytes.fromhex('1c0111001f010100061a024b53535009181c')
    s2 = bytes.fromhex('686974207468652062756c6c277320657965')

    s3 = '746865206b696420646f6e277420706c6179'.upper().encode()
    print(base64.b16encode(xorBytes(s1, s2)) == s3)
