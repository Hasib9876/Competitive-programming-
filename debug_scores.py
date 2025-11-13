#!/usr/bin/env python3
from collections import Counter

cipher = open("XOR.zip.crypt", 'rb').read()
actual_key = bytes.fromhex("d1c3795e520eea3afd00b604")

KEYLEN = 12
SIGNATURES = [b'PK\x03\x04', b'PK\x01\x02', b'PK\x05\x06']

n = len(cipher)
key_candidates = {i: {} for i in range(KEYLEN)}

for pos in range(n - 3):
    for sig in SIGNATURES:
        if pos + 4 > n:
            continue
        for i in range(4):
            idx = (pos + i) % KEYLEN
            proposed = cipher[pos + i] ^ sig[i]
            if proposed not in key_candidates[idx]:
                key_candidates[idx][proposed] = []
            key_candidates[idx][proposed].append((pos, sig))

counters = {i: Counter() for i in range(KEYLEN)}

for idx in range(KEYLEN):
    for byte_val, positions in key_candidates[idx].items():
        score = len(positions)
        for pos, sig in positions:
            if pos == 0 and sig == b'PK\x03\x04':
                score += 100
            elif pos < 10:
                score += 10
            elif pos < 200:
                score += 2
        counters[idx][byte_val] = score

print("Actual key:", actual_key.hex())
print("\nScores for each position:")
for i in range(KEYLEN):
    actual_byte = actual_key[i]
    actual_score = counters[i].get(actual_byte, 0)
    top_items = counters[i].most_common(3)
    print(f"\nPosition {i}: actual byte={actual_byte:02x}, score={actual_score}")
    print(f"  Top 3: {[(f'{b:02x}', s) for b, s in top_items]}")
    if actual_byte in [b for b, s in top_items]:
        rank = [b for b, s in counters[i].most_common()].index(actual_byte) + 1
        print(f"  Actual byte rank: {rank}")
