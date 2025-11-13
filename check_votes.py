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

# Find candidates and accumulate votes
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
        
        if mismatches == 0:
            if matches >= 2:
                weight = 10000 * (matches ** 2)
                for idx, proposed in proposed_bytes:
                    counters[idx][proposed] += weight
                    if partial_key[idx] is None:
                        partial_key[idx] = proposed
            elif matches == total_known and total_known > 0:
                weight = 5000
                for idx, proposed in proposed_bytes:
                    counters[idx][proposed] += weight
                    if partial_key[idx] is None:
                        partial_key[idx] = proposed
            elif total_known == 0:
                if pos < n / 2:
                    weight = 50
                else:
                    weight = 20
                for idx, proposed in proposed_bytes:
                    counters[idx][proposed] += weight

print("Votes for key indices 6-9 (where position 6 and 270 differ):")
for idx in [6, 7, 8, 9]:
    print(f"\nIndex {idx} (actual={actual_key[idx]:02x}):")
    top5 = counters[idx].most_common(5)
    for byte_val, count in top5:
        mark = " <-- ACTUAL" if byte_val == actual_key[idx] else ""
        print(f"  {byte_val:02x}: {count}{mark}")
