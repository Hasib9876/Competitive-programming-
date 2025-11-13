#!/usr/bin/env python3
from collections import Counter

cipher = open("XOR.zip.crypt", 'rb').read()
actual_key = bytes.fromhex("d1c3795e520eea3afd00b604")

KEYLEN = 12
SIGNATURES = [b'PK\x03\x04', b'PK\x01\x02', b'PK\x05\x06']
n = len(cipher)

counters = {i: Counter() for i in range(KEYLEN)}

# Just accumulate all weights
for pos in range(n - 3):
    for sig in SIGNATURES:
        if pos + 4 > n:
            continue
        for i in range(4):
            idx = (pos + i) % KEYLEN
            proposed = cipher[pos + i] ^ sig[i]
            
            # Weight based on position
            weight = 1
            if pos == 0:
                weight = 100
            elif pos < 10:
                weight = 10
            elif pos < 200:
                weight = 5
            
            counters[idx][proposed] += weight

print("Actual key:", actual_key.hex())
print("\nTop candidates per position:")
for i in range(KEYLEN):
    actual_byte = actual_key[i]
    top3 = counters[i].most_common(3)
    print(f"  {i}: {[(f'{b:02x}', w) for b, w in top3]}, actual={actual_byte:02x} rank={[b for b, w in counters[i].most_common()].index(actual_byte) + 1 if actual_byte in [b for b, w in counters[i].most_common()] else 'N/A'}")
