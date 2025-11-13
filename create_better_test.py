#!/usr/bin/env python3
"""
Create a better test case with a larger ZIP file that has more structure.
"""
import zipfile
import os

# Create a larger ZIP file with more content
zip_filename = "test_large.zip"
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Add multiple files to create more ZIP structure
    for i in range(5):
        content = f"This is test file number {i}.\n" * 20
        zf.writestr(f"file{i}.txt", content)

# Read the ZIP file
with open(zip_filename, 'rb') as f:
    plaintext = f.read()

print(f"Created ZIP file with {len(plaintext)} bytes")
print(f"First 64 bytes (hex): {plaintext[:64].hex()}")

# Use the SAME 12-byte XOR key from before
key = bytes.fromhex("d1c3795e520eea3afd00b604")
print(f"XOR Key (hex): {key.hex()}")

# Encrypt the ZIP file
def xor_encrypt(data, key):
    klen = len(key)
    return bytes(b ^ key[i % klen] for i, b in enumerate(data))

ciphertext = xor_encrypt(plaintext, key)

# Write the encrypted file
with open("XOR.zip.crypt", 'wb') as f:
    f.write(ciphertext)

print(f"Created encrypted file XOR.zip.crypt with {len(ciphertext)} bytes")

# Clean up the original ZIP
os.remove(zip_filename)
print("Test data created successfully!")
