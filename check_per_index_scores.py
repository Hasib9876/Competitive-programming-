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

# Calculate per-index consistency scores
pos_scores = {}
for pos, cands in pos_groups.items():
    index_agreements = []
    for key_idx in range(KEYLEN):
        proposals_for_idx = {}
        for cand in cands:
            for idx, proposed in cand['proposed_bytes']:
                if idx == key_idx:
                    proposals_for_idx[proposed] = proposals_for_idx.get(proposed, 0) + 1
        
        if proposals_for_idx:
            max_agreement = max(proposals_for_idx.values())
            index_agreements.append(max_agreement)
    
    pos_scores[pos] = (sum(index_agreements), index_agreements)

# Show top positions
sorted_positions = sorted(pos_scores.items(), key=lambda x: -x[1][0])
print("Top 15 positions by per-index consistency:")
for pos, (score, agreements) in sorted_positions[:15]:
    print(f"  Pos {pos}: total_score={score}, agreements={agreements}")

print(f"\nPosition 270: score={pos_scores.get(270, (0, []))}")
print(f"Position 6: score={pos_scores.get(6, (0, []))}")
