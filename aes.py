import base64

from Crypto.Cipher import AES

if __name__ == '__main__':
    key = 'YELLOW SUBMARINE'
    cipher = AES.new(key)
    with open('aes_ecb.txt') as f:
        text = ''.join(f.read().strip()).encode()
        text = base64.b64decode(text)
        print(cipher.decrypt(text))
