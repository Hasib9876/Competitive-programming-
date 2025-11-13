# XOR Key Recovery Tool

## Overview

This tool recovers a 12-byte repeating XOR key used to encrypt a ZIP file. It works by exploiting the known structure of ZIP files, which contain predictable byte signatures like `PK\x03\x04` (local file header), `PK\x01\x02` (central directory), and `PK\x05\x06` (end of central directory).

## Files

- `recover_xor_key.py` - Main recovery script
- `XOR.zip.crypt` - Example encrypted ZIP file (input)
- `XOR.key` - Recovered 12-byte key in hex format (output)
- `XOR_decrypted.zip` - Decrypted ZIP file (output)

## How It Works

1. **Candidate Generation**: The script scans every position in the ciphertext, assuming each of the three ZIP signatures could occur there. For each assumed signature at position `pos`, it computes what key bytes would be needed to produce that signature.

2. **Frequency Analysis**: Key byte candidates are weighted by frequency and position. Positions at the start of the file (which almost certainly contain `PK\x03\x04`) receive very high weight.

3. **Combinatorial Search**: The script tries combinations of the top-ranked candidates for each key byte position, validating each combination by decrypting and checking for valid ZIP structure.

## Usage

```bash
python3 recover_xor_key.py
```

The script expects `XOR.zip.crypt` to exist in the current directory and will produce:
- `XOR.key` - The recovered key in hexadecimal format
- `XOR_decrypted.zip` - The decrypted ZIP file

## Example Output

```
Read 236 bytes of ciphertext.
Most-common key guess (hex): d1c3795e520eea3afd00b604
Most-common guess validated as plausible key.
Wrote key to XOR.key and decrypted file to XOR_decrypted.zip.
```

## Testing

To create test data:

```bash
python3 create_user_testcase.py
```

This creates a sample encrypted ZIP file for testing the recovery process.

## Limitations

The success of key recovery depends on:
1. **File size**: Larger files provide more constraints and better statistics
2. **ZIP structure**: Files with multiple entries provide more signature matches
3. **Key properties**: Some keys may produce false positives that rank higher than the correct bytes

For difficult cases, you may need to:
- Increase `max_combinations` in `try_small_search()`
- Add additional known plaintext constraints
- Manually inspect the "Top candidates per key byte" output and try promising combinations

## Key Recovery Details

For the example file:
- **Actual Key**: `d1c3795e520eea3afd00b604`
- **File Size**: 236 bytes  
- **Recovered**: Successfully via position 0 analysis + combinatorial search

The recovery works because ZIP files have a very predictable structure, and the repeating 12-byte XOR key creates patterns that can be statistically analyzed.
