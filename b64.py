#!/usr/bin/python3

import base64

hexString = ('49276d206b696c6c696e6720796f757220627261696e206c696b65206'
             '120706f69736f6e6f7573206d757368726f6f6d')
theBytes = bytes.fromhex(hexString)
conversion = (b'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11'
              b'c2hyb29t')
b64 = base64.b64encode(theBytes)
print(b64 == conversion)
print(base64.b64decode(b64) == theBytes)
