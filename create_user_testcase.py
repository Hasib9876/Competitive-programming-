#!/usr/bin/env python3
"""
Create a 229-byte encrypted ZIP file similar to what the user has.
"""
import zipfile
import os

# Create a tiny ZIP file
zip_filename = "tiny_test.zip"
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_STORED) as zf:
    # Add one small file with no compression
    zf.writestr("test.txt", "Hello World!")

# Read the ZIP file
with open(zip_filename, 'rb') as f:
    plaintext = f.read()

# Pad or trim to approximately 229 bytes
if len(plaintext) < 229:
    # Add more files
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_STORED) as zf:
        zf.writestr("a.txt", "File A content here")
        zf.writestr("b.txt", "File B content here too")
    with open(zip_filename, 'rb') as f:
        plaintext = f.read()

print(f"Created ZIP file with {len(plaintext)} bytes")

# Use a simpler key that will be easier to recover
key = bytes.fromhex("d1c3795e520eea3afd00b604")
print(f"XOR Key (hex): {key.hex()}")

# Encrypt
def xor_encrypt(data, key):
    klen = len(key)
    return bytes(b ^ key[i % klen] for i, b in enumerate(data))

ciphertext = xor_encrypt(plaintext, key)

# Write
with open("XOR.zip.crypt", 'wb') as f:
    f.write(ciphertext)

print(f"Created XOR.zip.crypt with {len(ciphertext)} bytes")

# Clean up
os.remove(zip_filename)
print("Ready!")
