#!/usr/bin/env python3

cipher = open("XOR.zip.crypt", 'rb').read()

KEYLEN = 12
SIGNATURES = [b'PK\x03\x04', b'PK\x01\x02', b'PK\x05\x06']
n = len(cipher)

partial_key = list(bytes.fromhex("d1c3795e520e")) + [None] * 6

# Find unknown candidates
unknown_cands = []
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
            unknown_cands.append({
                'pos': pos,
                'sig': sig,
                'proposed_bytes': proposed_bytes
            })

# Group by position
pos_groups = {}
for cand in unknown_cands:
    pos = cand['pos']
    if pos not in pos_groups:
        pos_groups[pos] = []
    pos_groups[pos].append(cand)

# Calculate consistency scores
pos_scores = {}
for pos, cands in pos_groups.items():
    byte_proposals = {}
    for cand in cands:
        key = tuple(p for _, p in cand['proposed_bytes'])
        byte_proposals[key] = byte_proposals.get(key, 0) + 1
    
    max_agreement = max(byte_proposals.values()) if byte_proposals else 0
    pos_scores[pos] = (max_agreement, byte_proposals)

# Show top positions by consistency
sorted_positions = sorted(pos_scores.items(), key=lambda x: -x[1][0])
print("Top 10 positions by consistency score:")
for pos, (score, proposals) in sorted_positions[:10]:
    print(f"  Pos {pos}: consistency={score}")
    for prop_key, count in sorted(proposals.items(), key=lambda x: -x[1])[:2]:
        print(f"    {[f'{b:02x}' for b in prop_key]}: {count} times")
