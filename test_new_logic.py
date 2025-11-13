#!/usr/bin/env python3
from collections import Counter

cipher = open("XOR.zip.crypt", 'rb').read()
actual_key = bytes.fromhex("d1c3795e520eea3afd00b604")

KEYLEN = 12
SIGNATURES = [b'PK\x03\x04', b'PK\x01\x02', b'PK\x05\x06']
n = len(cipher)

# Initialize with position 0
partial_key = [None] * KEYLEN
sig = b'PK\x03\x04'
for i in range(4):
    idx = i % KEYLEN
    proposed = cipher[i] ^ sig[i]
    partial_key[idx] = proposed

print("Initial partial key:", [f'{b:02x}' if b is not None else 'None' for b in partial_key])

# Try iterations
for iteration in range(5):
    print(f"\n--- Iteration {iteration} ---")
    found_new = False
    
    # Look at known signature positions
    test_positions = [158, 216, 270, 325]
    for pos in test_positions:
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
                if total_known >= 2:
                    print(f"  Pos {pos}, sig {sig[:2].hex()}: matches={matches}, known={total_known}, mismatches={mismatches} - EXPANDING")
                    for idx, proposed in proposed_bytes:
                        if partial_key[idx] is None:
                            partial_key[idx] = proposed
                            found_new = True
                            print(f"    Set key[{idx}] = {proposed:02x}")
                elif total_known == 0:
                    print(f"  Pos {pos}, sig {sig[:2].hex()}: matches={matches}, known={total_known}, mismatches={mismatches} - potential (not expanding yet)")
    
    print(f"Partial key: {[f'{b:02x}' if b is not None else 'None' for b in partial_key]}")
    
    if not found_new:
        print("No new bytes found, stopping")
        break

print(f"\nFinal partial key:  {bytes([b if b is not None else 0 for b in partial_key]).hex()}")
print(f"Actual key:         {actual_key.hex()}")
