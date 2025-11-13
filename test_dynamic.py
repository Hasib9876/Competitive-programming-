#!/usr/bin/env python3

cipher = open("XOR.zip.crypt", 'rb').read()
actual_key = bytes.fromhex("d1c3795e520eea3afd00b604")

KEYLEN = 12
SIGNATURES = [b'PK\x03\x04', b'PK\x01\x02', b'PK\x05\x06']
n = len(cipher)

# Initialize
partial_key = [None] * KEYLEN
sig = b'PK\x03\x04'
for i in range(4):
    idx = i % KEYLEN
    proposed = cipher[i] ^ sig[i]
    partial_key[idx] = proposed

print("Initial:", [f'{b:02x}' if b is not None else 'None' for b in partial_key])

# Iterative expansion
for pass_num in range(10):
    print(f"\n--- Pass {pass_num} ---")
    made_progress = False
    
    # Rebuild candidates
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
                    'proposed_bytes': proposed_bytes,
                    'matches': matches,
                    'total_known': total_known
                })
    
    signature_candidates.sort(key=lambda x: (-x['matches'], -x['total_known'], x['pos']))
    
    print(f"  Found {len(signature_candidates)} candidates")
    print(f"  Top candidate: pos={signature_candidates[0]['pos']}, matches={signature_candidates[0]['matches']}, known={signature_candidates[0]['total_known']}")
    
    # Expand
    for cand in signature_candidates:
        if cand['matches'] >= 2 or (cand['matches'] == cand['total_known'] and cand['total_known'] > 0):
            for idx, proposed in cand['proposed_bytes']:
                if partial_key[idx] is None:
                    partial_key[idx] = proposed
                    made_progress = True
                    print(f"  From pos {cand['pos']}: set key[{idx}] = {proposed:02x}")
            
            if made_progress:
                break
    
    print(f"  Partial key: {[f'{b:02x}' if b is not None else 'None' for b in partial_key]}")
    
    if not made_progress:
        print("  No progress")
        break

print(f"\nFinal:  {bytes([b if b is not None else 0 for b in partial_key]).hex()}")
print(f"Actual: {actual_key.hex()}")
