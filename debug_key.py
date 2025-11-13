#!/usr/bin/env python3
# Check where the actual key bytes appear in the candidate lists

actual_key = bytes.fromhex("d1c3795e520eea3afd00b604")
print("Actual key (hex):", actual_key.hex())
print("Actual key bytes:", [f"{b:02x}" for b in actual_key])

# Top candidates from the output
candidates = [
    ["81", "9a", "a1", "f5", "f3", "e2"],  # 0: should be d1
    ["88", "93", "b3", "a8", "e7", "e1"],  # 1: should be c3
    ["29", "32", "7d", "7b", "79", "7f"],  # 2: should be 79
    ["15", "0e", "5a", "58", "5f", "5d"],  # 3: should be 5e
    ["02", "19", "76", "6d", "50", "7a"],  # 4: should be 52
    ["45", "5e", "7e", "65", "2c", "0c"],  # 5: should be 0e
    ["ba", "a1", "ee", "e8", "ec", "e9"],  # 6: should be ea
    ["71", "6a", "3e", "38", "3c", "39"],  # 7: should be 3a
    ["b6", "ad", "ff", "f9", "fe", "f8"],  # 8: should be fd
    ["4b", "50", "70", "6b", "04", "06"],  # 9: should be 00
    ["e6", "fd", "92", "b2", "89", "d3"],  # 10: should be b6
    ["4f", "54", "00", "20", "06", "02"],  # 11: should be 04
]

for i, (actual_byte, cands) in enumerate(zip(actual_key, candidates)):
    actual_hex = f"{actual_byte:02x}"
    if actual_hex in cands:
        pos = cands.index(actual_hex) + 1
        print(f"Position {i}: actual={actual_hex}, rank={pos}/{len(cands)}")
    else:
        print(f"Position {i}: actual={actual_hex}, NOT IN TOP 6!")
