import hashlib
import hmac
import math
import random
import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises")]

import aead  # noqa: E402
import aes  # noqa: E402
import chacha20  # noqa: E402
import ex5_ctr_bug  # noqa: E402
import ex6_cbc  # noqa: E402
import ex10_iv_game  # noqa: E402
import ex12_poly1305  # noqa: E402
import modes  # noqa: E402
import sha256  # noqa: E402

KEY = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
IV = bytes(range(16))
P = bytes.fromhex(
    "6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e51"
    "30c81c46a35ce411e5fbc1191a0a52eff69f2445df4f9b17ad2b417be66c3710"
)
C_CBC = bytes.fromhex(  # NIST SP 800-38A, F.2.1
    "7649abac8119b246cee98e9b12e9197d5086cb9b507219ee95db113a917678b2"
    "73bed6b8e3c1743b7116e69e222295163ff1caa1681fac09120eca307586e1a7"
)


def test_aes_and_modes_against_standards():
    plain = bytes.fromhex("3243f6a8885a308d313198a2e0370734")
    assert aes.encrypt_block(KEY, plain).hex() == "3925841d02dc09fbdc118597196a0b32"
    assert aes.SBOX[0x53] == 0xED and len(set(aes.SBOX)) == 256
    assert modes.cbc_encrypt(KEY, IV, P) == C_CBC
    assert modes.cbc_decrypt(KEY, IV, C_CBC) == P
    ctr = modes.ctr(KEY, bytes.fromhex("f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff"), P[:16])
    assert ctr.hex() == "874d6191b620e3261bef6864990db6ce"  # SP 800-38A, F.5.1


@settings(max_examples=30, deadline=None)
@given(st.binary(min_size=16, max_size=16), st.binary(max_size=40))
def test_roundtrips(key, m):
    assert aes.decrypt_block(key, aes.encrypt_block(key, IV)) == IV
    assert (
        modes.unpad(
            modes.cbc_decrypt(key, IV, modes.cbc_encrypt(key, IV, modes.pad(m)))
        )
        == m
    )
    assert (
        ex6_cbc.cbc_decrypt_checked(key, IV, modes.cbc_encrypt(key, IV, modes.pad(m)))
        == m
    )
    assert modes.ctr(key, IV, modes.ctr(key, IV, m)) == m
    assert len(modes.pad(m)) == 16 * (len(m) // 16 + 1)  # exercise 9


def test_ex6_on_the_vector_and_refusals():
    c = modes.cbc_encrypt(KEY, IV, P + bytes([16]) * 16)
    assert ex6_cbc.cbc_decrypt_checked(KEY, IV, c) == P
    for bad in (C_CBC[:15], b"", C_CBC):  # wrong length, empty, last byte 0x10 without 16 bytes of padding
        try:
            ex6_cbc.cbc_decrypt_checked(KEY, IV, bad)
            raise AssertionError("accepted")
        except ValueError:
            pass


def test_chacha_poly_aead():
    assert (
        ex12_poly1305.poly1305(
            bytes.fromhex(
                "85d6be7857556d337f4452fe42d506a80103808afb0db2fd4abff6af4149f51b"
            ),
            b"Cryptographic Forum Research Group",
        ).hex()
        == "a8061dc1305136c6c22b8baf0c0127a9"
    )
    key = bytes(range(0x80, 0xA0))
    nonce = bytes.fromhex("07000000") + bytes(range(0x40, 0x48))
    aad = bytes.fromhex("50515253c0c1c2c3c4c5c6c7")
    plain = (
        b"Ladies and Gentlemen of the class of '99: If I could offer you only"
        b" one tip for the future, sunscreen would be it."
    )
    c, t = aead.seal(key, nonce, aad, plain)
    assert c.hex().startswith("d31a8d34648e60db7b86afbc53ef7ec2") and c.hex().endswith(
        "6116"
    )
    assert t.hex() == "1ae10b594f09e26a7e902ecbd0600691"
    for i in range(len(c)):
        bad = bytearray(c)
        bad[i] ^= 0x80
        try:
            aead.open_(key, nonce, aad, bytes(bad), t)
            raise AssertionError("tampering accepted")
        except ValueError:
            pass
    assert (
        chacha20.chacha20(key, 1, nonce, chacha20.chacha20(key, 1, nonce, plain))
        == plain
    )


@settings(max_examples=50, deadline=None)
@given(st.binary(max_size=200))
def test_sha256_and_length_extension(m):
    assert sha256.sha256(m) == hashlib.sha256(m).digest()
    key, extra = b"k" * 16, b"&more"
    glue = sha256.pad(16 + len(m))
    state = [
        int.from_bytes(sha256.sha256(key + m)[i : i + 4], "big")
        for i in range(0, 32, 4)
    ]
    forged = sha256.sha256(extra, state, done=16 + len(m) + len(glue))
    assert forged == hashlib.sha256(key + m + glue + extra).digest()


def test_exercises_and_problem_numbers():
    k = bytes(range(16))
    m1, m2 = b"return book 42 by friday", b"the reading room is shut"
    x = modes.xor(ex5_ctr_bug.encrypt_buggy(k, m1), ex5_ctr_bug.encrypt_buggy(k, m2))
    assert x == modes.xor(m1, m2)
    assert sum(ex10_iv_game.play(s) for s in range(200)) == 200
    assert round(math.sqrt(math.pi / 2 * 2**32)) == 82137
    assert round(math.sqrt(math.pi / 2 * 2**64) / 1e9, 2) == 5.38  # exercise 3
    # problem: q = 10^9 records, collision chance q^2 / 2^(b+1) <= 10^-6
    bits = math.ceil(math.log2(1e18 / 2e-6))
    assert bits == 79
    assert round(1e18 / 2**65, 3) == 0.027  # 64 bits: about 2.7 %
    p = 1 - math.exp(-1e18 / 2**65)
    assert round(p, 4) == 0.0267
    # exercise 8: the union bound q(q-1)/2N is an upper bound
    rng = random.Random(3)
    n, q, trials = 1000, 30, 4000
    hits = sum(len({rng.randrange(n) for _ in range(q)}) < q for _ in range(trials))
    assert hits / trials <= q * (q - 1) / (2 * n) + 0.02


def test_hmac_matches_rfc2104_structure():
    key, m = b"key", b"The quick brown fox jumps over the lazy dog"
    k = key + bytes(64 - len(key))
    inner = hashlib.sha256(bytes(b ^ 0x36 for b in k) + m).digest()
    outer = hashlib.sha256(bytes(b ^ 0x5C for b in k) + inner).digest()
    assert outer == hmac.new(key, m, hashlib.sha256).digest()


def test_two_aes_rounds_make_every_byte_depend_on_every_byte():
    deps = [
        {i} for i in range(16)
    ]  # byte i of the state depends on input bytes deps[i]
    for _ in range(2):
        deps = [deps[j] for j in range(16)]
        rows = [[deps[r + 4 * c] for c in range(4)] for r in range(4)]
        shifted = [None] * 16
        for r in range(4):
            for c in range(4):
                shifted[r + 4 * c] = rows[r][(c + r) % 4]
        deps = [
            set().union(*shifted[4 * c : 4 * c + 4])
            for c in range(16 // 4)
            for _ in range(4)
        ]
    assert all(d == set(range(16)) for d in deps)
    # and in the real cipher: one flipped input byte changes all 16 bytes after 2 rounds
    k = aes.round_keys(KEY)

    def two_rounds(b):
        s = aes.add_round_key(list(b), k[0])
        for r in (1, 2):
            s = aes.add_round_key(
                aes.mix_columns(aes.shift_rows(aes.sub_bytes(s))), k[r]
            )
        return s

    a, b = two_rounds(bytes(16)), two_rounds(bytes([1]) + bytes(15))
    assert all(x != y for x, y in zip(a, b))


def test_vigenere_is_not_perfectly_secret_but_the_letter_pad_is():
    from collections import Counter
    from itertools import product

    def dist(m, keys):
        return Counter(
            tuple((x + k[i % len(k)]) % 26 for i, x in enumerate(m)) for k in keys
        )

    pad_keys = list(product(range(26), repeat=2))
    assert dist((0, 0), pad_keys) == dist((0, 1), pad_keys)  # exercise 7, letter pad
    vig_keys = [(k,) for k in range(26)]  # key length 1, messages of length 2
    assert dist((0, 0), vig_keys) != dist((0, 1), vig_keys)


def test_solution_numbers():
    n = 2**32
    assert round(math.exp(-10000 * 9999 / (2 * n)), 3) == 0.988
    assert round(math.exp(-100000 * 99999 / (2 * n)), 3) == 0.312
    assert round(1 - math.exp(-60000 * 59999 / (2 * n)), 2) == 0.34
    assert round(math.sqrt(2 * n * math.log(2))) == 77163
    assert round(math.sqrt(2 * 2**64 * math.log(2)) / 1e9, 2) == 5.06
    sd = math.sqrt((2 - math.pi / 2) * n)
    assert round(sd, -2) == 42900 and round(sd / math.sqrt(200), -2) == 3000
    assert round((78631 - 82137) / 82137 * 100, 1) == -4.3
    assert round(1 - math.exp(-0.5), 2) == 0.39
    assert hashlib.sha256(b"run 0 record 52355").digest()[:4].hex() == "3ae0cfc8"
    assert hashlib.sha256(b"run 0 record 53449").digest()[:4].hex() == "3ae0cfc8"
    for length, blocks, padbytes in (
        (0, 1, 16),
        (1, 1, 15),
        (15, 1, 1),
        (16, 2, 16),
        (17, 2, 15),
        (100, 7, 12),
    ):
        p = modes.pad(bytes(length))
        assert len(p) // 16 == blocks and p[-1] == padbytes
    assert bytes.fromhex("b6") == bytes([0b10110110])
    assert (
        0b10110110 ^ 0b01101100 == 0b11011010 and 0b11011010 ^ 0b00001111 == 0b11010101
    )
