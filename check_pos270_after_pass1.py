#!/usr/bin/env python3

cipher = open("XOR.zip.crypt", 'rb').read()
n = len(cipher)

# After pass 1, partial_key should have indices 0-5 filled
partial_key = list(bytes.fromhex("d1c3795e520e")) + [None] * 6

pos = 270
sig = b'PK\x01\x02'

print(f"Position {pos}, signature {sig.hex()}")
print(f"Partial key: {[f'{b:02x}' if b is not None else 'None' for b in partial_key]}")

matches = 0
total_known = 0
mismatches = 0

for i in range(4):
    idx = (pos + i) % 12
    proposed = cipher[pos + i] ^ sig[i]
    known_val = partial_key[idx]
    
    print(f"  i={i}, idx={idx}, proposed={proposed:02x}, known={f'{known_val:02x}' if known_val is not None else 'None'}", end="")
    
    if known_val is not None:
        total_known += 1
        if known_val == proposed:
            matches += 1
            print(" - MATCH")
        else:
            mismatches += 1
            print(" - MISMATCH")
    else:
        print(" - unknown")

print(f"\nSummary: matches={matches}, known={total_known}, mismatches={mismatches}")
print(f"Condition: matches >= 2? {matches >= 2}")
print(f"Condition: matches == total_known and total_known > 0? {matches == total_known and total_known > 0}")
