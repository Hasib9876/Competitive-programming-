#!/usr/bin/env python3
cipher = open("XOR.zip.crypt", 'rb').read()
actual_key = bytes.fromhex("d1c3795e520eea3afd00b604")

# Position 158 should have PK\x03\x04
pos = 158
sig = b'PK\x03\x04'
print(f"Position {pos} cipher bytes: {cipher[pos:pos+4].hex()}")
print(f"Key indices at pos {pos}: {[(pos+i)%12 for i in range(4)]}")
print(f"Expected key bytes: {[cipher[pos+i] ^ sig[i] for i in range(4)]}")
print(f"Expected key (hex): {bytes([cipher[pos+i] ^ sig[i] for i in range(4)]).hex()}")
print(f"Actual key at those positions: {bytes([actual_key[(pos+i)%12] for i in range(4)]).hex()}")

# Check if the constraint propagation would have identified this
partial_key = [actual_key[i] for i in range(4)] + [None] * 8
print(f"\nPartial key after position 0: {[f'{b:02x}' if b is not None else 'None' for b in partial_key]}")

matches = 0
for i in range(4):
    idx = (pos + i) % 12
    proposed = cipher[pos + i] ^ sig[i]
    if partial_key[idx] is not None and partial_key[idx] == proposed:
        matches += 1
        print(f"  Index {idx}: matches! (proposed {proposed:02x} == partial {partial_key[idx]:02x})")
    else:
        print(f"  Index {idx}: no match (proposed {proposed:02x}, partial {partial_key[idx] if partial_key[idx] is not None else 'None'})")

print(f"\nTotal matches at position {pos}: {matches}")
