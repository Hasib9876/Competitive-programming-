#!/usr/bin/env python3
# Analyze the encrypted ZIP file to understand the structure

with open("XOR.zip.crypt", 'rb') as f:
    cipher = f.read()

print(f"Ciphertext length: {len(cipher)} bytes")
print(f"First 64 bytes (hex): {cipher[:64].hex()}")

# The actual key
key = bytes.fromhex("d1c3795e520eea3afd00b604")

# Decrypt to see the plaintext
def xor_decrypt(data, key):
    klen = len(key)
    return bytes(b ^ key[i % klen] for i, b in enumerate(data))

plaintext = xor_decrypt(cipher, key)
print(f"\nPlaintext first 64 bytes (hex): {plaintext[:64].hex()}")
print(f"Plaintext as string: {plaintext[:64]}")

# Find all PK signatures in plaintext
import re
for sig_name, sig in [("PK\\x03\\x04", b'PK\x03\x04'), ("PK\\x01\\x02", b'PK\x01\x02'), ("PK\\x05\\x06", b'PK\x05\x06')]:
    positions = [m.start() for m in re.finditer(re.escape(sig), plaintext)]
    print(f"\nSignature {sig_name} found at positions: {positions}")
    for pos in positions:
        print(f"  Position {pos}: cipher bytes = {cipher[pos:pos+4].hex()}")
        print(f"  Position {pos}: key indices = {[(pos+i)%12 for i in range(4)]}")
        print(f"  Position {pos}: expected key bytes = {[cipher[pos+i] ^ sig[i] for i in range(4)]}")
