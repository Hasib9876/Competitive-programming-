# XOR Key Recovery Tool

This tool recovers a 12-byte repeating XOR key used to encrypt a ZIP file using known plaintext attack.

## How It Works

The ZIP file format contains well-known 4-byte signatures:
- Local file header: `PK\x03\x04` (50 4B 03 04)
- Central directory: `PK\x01\x02` (50 4B 01 02)
- End of central directory: `PK\x05\x06` (50 4B 05 06)

When a ZIP file is encrypted with a repeating 12-byte XOR key, we can:
1. Scan the ciphertext for all possible signature locations
2. For each location, compute what the key bytes would need to be
3. Use frequency analysis to find the most likely key
4. Validate the key by checking if decryption produces valid ZIP signatures

## Usage

### Prerequisites
- Python 3.6 or higher
- Input file: `XOR.zip.crypt` (the encrypted ZIP file)

### Running the Script

```bash
python3 xor_key_recovery.py
```

### Output Files

If successful, the script creates:
- `XOR.key` - The recovered 12-byte key (hex encoded)
- `XOR_decrypted.zip` - The decrypted ZIP file

### Example

```bash
# Place your encrypted file
cp /path/to/encrypted/file XOR.zip.crypt

# Run the recovery script
python3 xor_key_recovery.py

# Output:
# Read 1234 bytes of ciphertext.
# Most-common key guess (hex): 414243444546474849...
# Most-common guess validated as plausible key.
# Wrote key to XOR.key and decrypted file to XOR_decrypted.zip.
# Quick verification: first bytes of decrypted file: b'PK\x03\x04...'

# Extract the decrypted ZIP
unzip XOR_decrypted.zip
```

## Algorithm Details

### Step 1: Gather Candidate Key Bytes
For every position in the ciphertext and every known signature, compute what key bytes would produce that signature at that position.

### Step 2: Frequency Analysis
Count occurrences of each candidate byte for each of the 12 key positions. The most frequent candidate is likely correct.

### Step 3: Validation
Decrypt with the candidate key and check for:
- Presence of `PK\x03\x04` (local file header)
- Presence of `PK\x05\x06` (end of central directory)

### Step 4: Combinatorial Search (Fallback)
If the most common key doesn't validate, try combinations of the top 2 candidates for each position (limited to 2000 combinations).

## Limitations

- Requires the ciphertext to be a XOR-encrypted ZIP file
- Key must be exactly 12 bytes and repeating
- Works best with ZIP files that have standard structure
- May fail if the ZIP file is too small or has unusual structure

## Troubleshooting

**"Missing ciphertext file: XOR.zip.crypt"**
- Ensure the encrypted file is named `XOR.zip.crypt` and in the current directory

**"No plausible key found"**
- The file may not be a ZIP file encrypted with a 12-byte repeating XOR key
- Try increasing `max_combinations` in the `try_small_search` function
- Examine the "Top candidates per key byte" output for manual analysis

## Security Note

This tool demonstrates a known-plaintext attack on XOR encryption. XOR with a short repeating key is **not secure** for protecting sensitive data. This is for educational and CTF purposes only.
