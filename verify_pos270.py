#!/usr/bin/env python3
cipher = open("XOR.zip.crypt", 'rb').read()
actual_key = bytes.fromhex("d1c3795e520eea3afd00b604")

# Position 270 should have PK\x01\x02
pos = 270
sig = b'PK\x01\x02'
print(f"Position {pos} cipher bytes: {cipher[pos:pos+4].hex()}")
print(f"Key indices at pos {pos}: {[(pos+i)%12 for i in range(4)]}")
print(f"Expected key bytes: {[cipher[pos+i] ^ sig[i] for i in range(4)]}")
print(f"Expected key (hex): {bytes([cipher[pos+i] ^ sig[i] for i in range(4)]).hex()}")
print(f"Actual key at those positions: {bytes([actual_key[(pos+i)%12] for i in range(4)]).hex()}")

# Check if the constraint propagation would have identified this
# After processing earlier signatures, we should have partial_key with indices 0-5 filled
partial_key_list = list(actual_key[:6]) + [None] * 6
partial_key = {i: partial_key_list[i] for i in range(12)}
print(f"\nPartial key after position 158: {[f'{partial_key[i]:02x}' if partial_key[i] is not None else 'None' for i in range(12)]}")

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
print(f"This should get high weight since matches = {matches}")
