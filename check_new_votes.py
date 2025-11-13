#!/usr/bin/env python3
from collections import Counter

cipher = open("XOR.zip.crypt", 'rb').read()
actual_key = bytes.fromhex("d1c3795e520eea3afd00b604")

KEYLEN = 12
SIGNATURES = [b'PK\x03\x04', b'PK\x01\x02', b'PK\x05\x06']
n = len(cipher)

counters = {i: Counter() for i in range(KEYLEN)}

# Position 0 init
partial_key = [None] * KEYLEN
sig = b'PK\x03\x04'
for i in range(4):
    idx = i % KEYLEN
    proposed = cipher[i] ^ sig[i]
    partial_key[idx] = proposed
    counters[idx][proposed] += 100000

# Accumulate votes
for pos in range(n - 3):
    for sig in SIGNATURES:
        if pos + 4 > n:
            continue
        
        matches = 0
        total_known = 0
        mismatches = 0
        proposed_bytes = []
        
        for i in range(4):
            idx = (pos + i) % KEYLEN
            proposed = cipher[pos + i] ^ sig[i]
            proposed_bytes.append((idx, proposed))
            
            if partial_key[idx] is not None:
                total_known += 1
                if partial_key[idx] == proposed:
                    matches += 1
                else:
                    mismatches += 1
        
        if mismatches == 0 and total_known == 0:
            if pos < 50:
                weight = 30
            elif pos < 200:
                weight = 100
            else:
                weight = 80
            
            for idx, proposed in proposed_bytes:
                counters[idx][proposed] += weight

print("Index 6 votes:")
for byte_val, count in counters[6].most_common(10):
    mark = " <-- ACTUAL" if byte_val == actual_key[6] else ""
    print(f"  {byte_val:02x}: {count}{mark}")
