#!/usr/bin/env python3
"""
Task 3 solution: recover a 12-byte repeating XOR key used to encrypt a ZIP file.

Approach:
 - The ZIP format contains well-known 4-byte signatures (local file header, central dir, end-of-central):
     b'PK\x03\x04', b'PK\x01\x02', b'PK\x05\x06'
 - If the ciphertext is produced by XORing the plaintext with a repeating 12-byte key,
   then at any file offset `pos` where plaintext has a known 4-byte signature `S`,
   we obtain 4 constraints on key bytes:
       key[(pos + i) % 12] = ciphertext[pos + i] ^ S[i], for i = 0..3
 - We scan the ciphertext for all offsets and for each signature derive many candidate
   values for each of the 12 key positions. We then pick the most-consistent candidate
   per key byte and try to validate the resulting key by decrypting and checking
   for ZIP signatures and plausible ZIP structure. If needed, we attempt a small
   combinatorial search among the top candidates per position.

Output:
 - Writes `XOR.key` (hex encoded 12-byte key) if found.
 - Writes `XOR_decrypted.zip` (decrypted zip) if a valid key is found.
"""

from pathlib import Path
from collections import Counter, defaultdict
import itertools

KEYLEN = 12
SIGNATURES = [b'PK\x03\x04', b'PK\x01\x02', b'PK\x05\x06']
CIPHER_NAME = "XOR.zip.crypt"
OUT_KEY_HEX = "XOR.key"
OUT_ZIP = "XOR_decrypted.zip"

def xor_decrypt_with_key_repeating(data: bytes, key: bytes) -> bytes:
    klen = len(key)
    return bytes(b ^ key[i % klen] for i, b in enumerate(data))

def gather_candidate_key_bytes(cipher: bytes):
    """
    Scan the ciphertext and collect candidate values for each key index (0..KEYLEN-1)
    by assuming each of the known signatures occurs at each offset.
    """
    counters = {i: Counter() for i in range(KEYLEN)}
    n = len(cipher)
    for pos in range(max(0, n - 4) + 1):
        # for each signature try to compute key fragment that would produce it
        for sig in SIGNATURES:
            if pos + 4 > n:
                continue
            # compute proposed key bytes for this placement
            for i in range(4):
                idx = (pos + i) % KEYLEN
                proposed = cipher[pos + i] ^ sig[i]
                counters[idx][proposed] += 1
    return counters

def choose_most_common_key(counters):
    # Pick the most common candidate for each key index
    key = bytearray(KEYLEN)
    candidates_per_index = []
    for i in range(KEYLEN):
        most_common = counters[i].most_common()
        if most_common:
            # get list of candidate bytes in order of frequency
            candidates_per_index.append([b for b, _count in most_common])
            key[i] = most_common[0][0]
        else:
            # no candidate: default to 0x00 (will be tried later in combinations)
            candidates_per_index.append([0])
            key[i] = 0
    return bytes(key), candidates_per_index

def validate_key(cipher: bytes, key: bytes) -> bool:
    dec = xor_decrypt_with_key_repeating(cipher, key)
    # simple sanity checks
    # Must contain local header at start (frequently at or near offset 0)
    if b'PK\x03\x04' not in dec:
        return False
    if b'PK\x05\x06' not in dec:
        return False
    # Further checks: end-of-central-directory record has comment length 0 (2 bytes) at offset
    # after signature + 18 bytes. We'll not strictly require that but presence of signatures is strong.
    return True

def try_small_search(cipher: bytes, candidates_per_index, max_combinations=2000):
    # We'll build a small cartesian product search over the top few candidates for each index,
    # limiting total combinations to max_combinations.
    # Choose top_n for each index to keep combination count reasonable.
    top_n = 2
    chosen_lists = []
    for lst in candidates_per_index:
        chosen_lists.append(lst[:top_n] if len(lst) >= top_n else lst)
    # estimate combinations
    total = 1
    for lst in chosen_lists:
        total *= len(lst)
        if total > max_combinations:
            break
    # If the product is still large, reduce top_n
    if total > max_combinations:
        top_n = 1
        chosen_lists = [lst[:top_n] for lst in candidates_per_index]
    # Now iterate combinations
    tried = 0
    for comb in itertools.product(*chosen_lists):
        tried += 1
        key = bytes(comb)
        if validate_key(cipher, key):
            return key
        if tried >= max_combinations:
            break
    return None

def main():
    p = Path(CIPHER_NAME)
    if not p.exists():
        print(f"Missing ciphertext file: {CIPHER_NAME}")
        return
    cipher = p.read_bytes()
    print(f"Read {len(cipher)} bytes of ciphertext.")

    counters = gather_candidate_key_bytes(cipher)
    key_guess, candidates_per_index = choose_most_common_key(counters)
    print("Most-common key guess (hex):", key_guess.hex())

    # Try validating the most-common key
    if validate_key(cipher, key_guess):
        print("Most-common guess validated as plausible key.")
        final_key = key_guess
    else:
        print("Most-common guess did not validate. Trying small combinatorial search among top candidates...")
        final_key = try_small_search(cipher, candidates_per_index)
        if final_key:
            print("Found plausible key via small search:", final_key.hex())
        else:
            print("No plausible key found by heuristic search. You may increase search scope or add more known plaintext constraints.")
            final_key = None

    if final_key:
        # write key file (hex)
        Path(OUT_KEY_HEX).write_text(final_key.hex())
        # write decrypted zip
        decrypted = xor_decrypt_with_key_repeating(cipher, final_key)
        Path(OUT_ZIP).write_bytes(decrypted)
        print(f"Wrote key to {OUT_KEY_HEX} and decrypted file to {OUT_ZIP}.")
        print("Quick verification: first bytes of decrypted file:", decrypted[:64])
        print("You should now be able to open the decrypted zip file with unzip or a GUI.")
    else:
        print("Failed to determine a key automatically. See script comments for further steps.")
        # For further manual analysis: print top candidates per key index for manual inspection
        print("\nTop candidates per key byte (index: byte(hex) count):")
        for i in range(KEYLEN):
            items = counters[i].most_common(6)
            s = ", ".join(f"{b:02x}({c})" for b, c in items)
            print(f"{i}: {s}")

if __name__ == "__main__":
    main()
