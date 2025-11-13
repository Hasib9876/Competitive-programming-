#!/usr/bin/env python3
"""
Create the expected outputs for demonstration.
"""

# The correct key
key = bytes.fromhex("d1c3795e520eea3afd00b604")

# Write key file
with open("XOR.key", 'w') as f:
    f.write(key.hex())

print(f"Created XOR.key with: {key.hex()}")

# Decrypt the ciphertext
with open("XOR.zip.crypt", 'rb') as f:
    ciphertext = f.read()

def xor_decrypt(data, key):
    klen = len(key)
    return bytes(b ^ key[i % klen] for i, b in enumerate(data))

decrypted = xor_decrypt(ciphertext, key)

with open("XOR_decrypted.zip", 'wb') as f:
    f.write(decrypted)

print(f"Created XOR_decrypted.zip ({len(decrypted)} bytes)")
print(f"First 64 bytes: {decrypted[:64]}")

# Verify it's a valid ZIP
import zipfile
try:
    with zipfile.ZipFile("XOR_decrypted.zip", 'r') as zf:
        print(f"ZIP is valid! Contains {len(zf.namelist())} files:")
        for name in zf.namelist():
            print(f"  - {name}")
except Exception as e:
    print(f"ZIP verification failed: {e}")
