from collections import Counter

def readBytes(filename, chunksize=8192):
    with open(filename, 'rb') as f:
        chunk = True
        while chunk:
            chunk = f.read(chunksize)
            yield chunk


if __name__ == '__main__':
    counter = Counter()
    for chunk in readBytes('english.txt'):
        counter.update(Counter(chunk))
    s = sum(counter.values())

    for k, v in counter.items():
        c = chr(k).lower()
        if c != chr(k):
            counter[ord(c)] += counter[k]
            counter[k] = 0

    for k, v in counter.items():
        if v: print('{} {}'.format(chr(k), v/s))
