#!/usr/bin/env python3
"""
Create test data for XOR key recovery script.
"""
import zipfile
import os
from pathlib import Path

# Create a simple ZIP file
zip_filename = "test.zip"
with zipfile.ZipFile(zip_filename, 'w') as zf:
    zf.writestr("test.txt", "This is a test file for XOR encryption.\n" * 3)
    zf.writestr("file2.txt", "Another test file.\n")

# Read the ZIP file
with open(zip_filename, 'rb') as f:
    plaintext = f.read()

print(f"Created ZIP file with {len(plaintext)} bytes")
print(f"First 64 bytes (hex): {plaintext[:64].hex()}")

# Use a 12-byte XOR key
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
print(f"First 64 bytes (hex): {ciphertext[:64].hex()}")

# Clean up the original ZIP
os.remove(zip_filename)
print("Test data created successfully!")
