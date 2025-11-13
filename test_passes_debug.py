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

# Passes
for pass_num in range(10):
    print(f"\n=== Pass {pass_num} ===")
    
    # After pass 2, check positions 6 and 270
    if pass_num == 2:
        for test_pos in [6, 270]:
            print(f"\nChecking position {test_pos}:")
            for sig in SIGNATURES:
                matches = 0
                mismatches = 0
                proposed_bytes = []
                for i in range(4):
                    idx = (test_pos + i) % KEYLEN
                    proposed = cipher[test_pos + i] ^ sig[i]
                    proposed_bytes.append((idx, proposed))
                    if partial_key[idx] is not None:
                        if partial_key[idx] == proposed:
                            matches += 1
                        else:
                            mismatches += 1
                
                if mismatches == 0:
                    print(f"  {sig[:2].hex()}: matches={matches}, proposed={[f'{b:02x}' for _, b in proposed_bytes]}")
    
    # Actually do the expansion logic...
    # (skipping implementation for brevity, just showing what positions would be chosen)
    
    if pass_num == 0:
        # Would accept position 325 (has matches=3)
        partial_key[4] = 0x52
        print("  Accepted pos 325, set key[4]=52")
    elif pass_num == 1:
        # Would accept position 158 (has matches=4 after key[4] is set)
        partial_key[5] = 0x0e
        print("  Accepted pos 158, set key[5]=0e")
    elif pass_num == 2:
        # Would accept position 6 (score=8, comes first)
        partial_key[6] = 0xba
        partial_key[7] = 0x71
        partial_key[8] = 0xfe
        partial_key[9] = 0x04
        print("  Accepted pos 6, set keys[6-9]")
        break
    
    print(f"Partial key: {[f'{b:02x}' if b is not None else 'None' for b in partial_key]}")

print(f"\nFinal:  {bytes([b if b is not None else 0 for b in partial_key]).hex()}")
print(f"Actual: {actual_key.hex()}")
