"""aes_vector.py -- the cipher example of FIPS 197, Appendix B, and its round keys."""

from aes import SBOX, decrypt_block, encrypt_block, round_keys

key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
plain = bytes.fromhex("3243f6a8885a308d313198a2e0370734")
cipher = encrypt_block(key, plain)
print("S-box of 00, 01, 53:", " ".join(f"{SBOX[a]:02x}" for a in (0x00, 0x01, 0x53)))
print("round key 1: ", bytes(round_keys(key)[1]).hex())
print("round key 10:", bytes(round_keys(key)[10]).hex())
print("ciphertext:  ", cipher.hex())
print("FIPS 197:    ", "3925841d02dc09fbdc118597196a0b32")
print("decrypts back:", decrypt_block(key, cipher) == plain)
