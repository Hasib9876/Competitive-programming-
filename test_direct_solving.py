#!/usr/bin/env python3

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

print("Initial:", [f'{b:02x}' if b is not None else 'None' for b in partial_key])

# Find all potential PK signature locations
signature_candidates = []
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
            signature_candidates.append({
                'pos': pos,
                'sig': sig,
                'proposed_bytes': proposed_bytes,
                'matches': matches,
                'total_known': total_known
            })

# Sort by matches
signature_candidates.sort(key=lambda x: (-x['matches'], -x['total_known'], x['pos']))

print(f"\nFound {len(signature_candidates)} consistent signature candidates")
print("Top 10:")
for i, cand in enumerate(signature_candidates[:10]):
    print(f"  {i}: pos={cand['pos']}, matches={cand['matches']}, known={cand['total_known']}, proposed={[f'{b:02x}' for _, b in cand['proposed_bytes']]}")

# Expand iteratively
for pass_num in range(10):
    made_progress = False
    print(f"\n--- Pass {pass_num} ---")
    
    for cand in signature_candidates:
        matches = 0
        total_known = 0
        mismatches = 0
        
        for idx, proposed in cand['proposed_bytes']:
            if partial_key[idx] is not None:
                total_known += 1
                if partial_key[idx] == proposed:
                    matches += 1
                else:
                    mismatches += 1
        
        if mismatches == 0 and matches >= 2:
            for idx, proposed in cand['proposed_bytes']:
                if partial_key[idx] is None:
                    partial_key[idx] = proposed
                    made_progress = True
                    print(f"  From pos {cand['pos']}: set key[{idx}] = {proposed:02x}")
    
    print(f"Partial key: {[f'{b:02x}' if b is not None else 'None' for b in partial_key]}")
    
    if not made_progress:
        print("No progress")
        break

print(f"\nFinal:  {bytes([b if b is not None else 0 for b in partial_key]).hex()}")
print(f"Actual: {actual_key.hex()}")
