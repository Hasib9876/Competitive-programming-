#!/usr/bin/env python3

cipher = open("XOR.zip.crypt", 'rb').read()
actual_key = bytes.fromhex("d1c3795e520eea3afd00b604")

KEYLEN = 12
SIGNATURES = [b'PK\x03\x04', b'PK\x01\x02', b'PK\x05\x06']
n = len(cipher)

# After pass 1, we should have
partial_key = list(bytes.fromhex("d1c3795e520e")) + [None] * 6

print(f"Starting pass 2 with: {[f'{b:02x}' if b is not None else 'None' for b in partial_key]}")

# Find candidates with total_known == 0
unknown_candidates = []
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
        
        if mismatches == 0 and total_known == 0 and pos < 400:
            unknown_candidates.append({
                'pos': pos,
                'sig': sig,
                'proposed_bytes': proposed_bytes,
                'indices': [(pos + i) % KEYLEN for i in range(4)]
            })

print(f"\nFound {len(unknown_candidates)} unknown candidates")
print("\nFirst 10 unknown candidates:")
for i, cand in enumerate(unknown_candidates[:10]):
    indices = cand['indices']
    proposed = [p for _, p in cand['proposed_bytes']]
    print(f"  {i}: pos={cand['pos']}, sig={cand['sig'][:2].hex()}, indices={indices}, proposed={[f'{b:02x}' for b in proposed]}")
    
    # Check if matches actual key
    actual_at_indices = [actual_key[idx] for idx in indices]
    if proposed == actual_at_indices:
        print(f"      *** MATCHES ACTUAL KEY! ***")

# Position 270 should be in this list
print("\nLooking for position 270:")
for cand in unknown_candidates:
    if cand['pos'] == 270:
        print(f"  Found! sig={cand['sig'].hex()}, indices={cand['indices']}, proposed={[f'{b:02x}' for _, b in cand['proposed_bytes']]}")
