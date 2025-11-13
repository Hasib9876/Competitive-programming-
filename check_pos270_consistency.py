#!/usr/bin/env python3

cipher = open("XOR.zip.crypt", 'rb').read()

SIGNATURES = [b'PK\x03\x04', b'PK\x01\x02', b'PK\x05\x06']
pos = 270

print(f"Position {pos}:")
for sig in SIGNATURES:
    proposed = []
    for i in range(4):
        idx = (pos + i) % 12
        p = cipher[pos + i] ^ sig[i]
        proposed.append(f"{p:02x}")
    print(f"  {sig.hex()}: {proposed}")
