import hashlib
import math
import random
import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises")]

import ec_add  # noqa: E402
import ex5_schnorr_range  # noqa: E402
import ex6_crt  # noqa: E402
import ex12_hkdf  # noqa: E402
import groups  # noqa: E402
import rsa  # noqa: E402
import schnorr  # noqa: E402
import toy_cert  # noqa: E402
from bsgs import bsgs  # noqa: E402


def test_miller_rabin_and_subgroups():
    rng = random.Random(1)
    small = [n for n in range(2, 2000) if groups.is_probable_prime(n, rng)]
    assert small == [
        n for n in range(2, 2000) if all(n % d for d in range(2, math.isqrt(n) + 1))
    ]
    assert not groups.is_probable_prime(561, rng)  # a Carmichael number
    p, q, g = groups.subgroup(32, 64, rng)
    assert (p - 1) % q == 0 and g != 1 and pow(g, q, p) == 1


@settings(max_examples=20, deadline=None)
@given(st.integers(min_value=0, max_value=2**31))
def test_bsgs_finds_every_log_within_2m(x):
    rng = random.Random(9)
    p, q, g = groups.subgroup(24, 48, rng)
    x %= q
    found, steps = bsgs(g, pow(g, x, p), p, q)
    m = math.isqrt(q - 1) + 1
    assert found == x and steps <= 2 * m


def test_rsa_roundtrip_crt_and_hand_example():
    pub, priv = rsa.keygen(512, random.Random(3))
    rng = random.Random(4)
    for _ in range(20):
        m = rng.randrange(pub["n"])
        c = rsa.encrypt(pub, m)
        assert rsa.decrypt(priv, c) == m == ex6_crt.decrypt_crt(priv, c)
    # messages sharing a factor with n (exercise 7)
    for m in (0, priv["p"], 5 * priv["q"]):
        assert rsa.decrypt(priv, rsa.encrypt(pub, m)) == m
    # exercise 2: p = 61, q = 53
    n, phi, e = 61 * 53, 60 * 52, 17
    d = pow(e, -1, phi)
    assert (n, d, pow(65, e, n), pow(2790, d, n)) == (3233, 2753, 2790, 65)


def test_dh_by_hand_exercise_1():
    p, g, a, b = 23, 4, 3, 7
    assert pow(g, 11, p) == 1
    A, B = pow(g, a, p), pow(g, b, p)
    assert (A, B, pow(B, a, p), pow(A, b, p)) == (18, 8, 6, 6)


def test_schnorr_sign_verify_reuse_and_range():
    rng = random.Random(11)
    x, y = schnorr.keygen(rng)
    for i in range(10):
        m = b"message %d" % i
        sig = schnorr.sign(x, m, rng)
        assert schnorr.verify(y, m, sig) and not schnorr.verify(y, m + b"!", sig)
        r, s = sig
        assert ex5_schnorr_range.verify_buggy(y, m, (r, s + schnorr.Q))
        assert not schnorr.verify(y, m, (r, s + schnorr.Q))
    k = 123456789  # exercise 11: two signatures with one nonce give x
    r = pow(schnorr.G, k, schnorr.P)
    e1, e2 = schnorr.challenge(r, b"a"), schnorr.challenge(r, b"b")
    s1, s2 = (k + e1 * x) % schnorr.Q, (k + e2 * x) % schnorr.Q
    assert (s1 - s2) * pow(e1 - e2, -1, schnorr.Q) % schnorr.Q == x


def test_certificates():
    rng = random.Random(12)
    rx, ry = schnorr.keygen(rng)
    lx, ly = schnorr.keygen(rng)
    leaf = toy_cert.make_cert("a.example", ly, "Root CA", rx, ca=False)
    assert toy_cert.check_chain([leaf], {"Root CA": ry}, "2026-06-01") == "ok"
    assert toy_cert.check_chain([leaf], {}, "2026-06-01").endswith("Root CA")
    bad = {"body": dict(leaf["body"], subject="b.example"), "sig": leaf["sig"]}
    assert toy_cert.check_chain([bad], {"Root CA": ry}, "2026-06-01").endswith(
        "bad signature"
    )


def test_hkdf_rfc5869_cases_1_to_3():
    okm1 = ex12_hkdf.hkdf(bytes(range(13)), b"\x0b" * 22, bytes(range(0xF0, 0xFA)), 42)
    assert okm1.hex() == (
        "3cb25f25faacd57a90434f64d0362f2a2d2d0a90cf1a5a4c"
        "5db02d56ecc4c5bf34007208d5b887185865"
    )
    okm2 = ex12_hkdf.hkdf(
        bytes(range(0x60, 0xB0)), bytes(range(0x50)), bytes(range(0xB0, 0x100)), 82
    )
    assert okm2.hex() == (
        "b11e398dc80327a1c8e7f78c596a49344f012eda2d4efad8a050cc4c19afa97c"
        "59045a99cac7827271cb41c65e590e09da3275600c2f09b8367793a9aca3db71"
        "cc30c58179ec3e87c14c01d5c1f3434f1d87"
    )
    prk3 = ex12_hkdf.extract(b"", b"\x0b" * 22)
    assert (
        prk3.hex() == "19ef24a32c717b167f33a91d6f648bdf96596776afdb6377ac434c1c293ccb04"
    )
    assert ex12_hkdf.expand(prk3, b"", 42).hex() == (
        "8da4e775a563c18f715f802a063c5a31b8a11f5c5ee1879ec3454e5f3c738d2d9d201395faa4b61a96c8"
    )


def test_elliptic_curve_group_laws():
    p, a, b = 97, 2, 3
    pts = [None] + [
        (x, y)
        for x in range(p)
        for y in range(p)
        if (y * y - x**3 - a * x - b) % p == 0
    ]
    assert len(pts) == 100 and abs(len(pts) - (p + 1)) <= 2 * math.sqrt(p)
    rng = random.Random(5)
    for _ in range(200):
        P, Q, R = rng.choice(pts), rng.choice(pts), rng.choice(pts)
        add = lambda u, v: ec_add.add(u, v, a, p)  # noqa: E731
        assert add(P, Q) == add(Q, P) and add(add(P, Q), R) == add(P, add(Q, R))
        assert add(P, Q) in pts


def test_numbers_quoted():
    q_bits_for_128 = 2 * 128
    assert q_bits_for_128 == 256
    assert round(2 * math.sqrt(2**36)) == 524288
    assert 128 * 8 * 2**14 == 16 * 2**20  # scrypt memory, 16 MiB
    assert hashlib.sha256(b"x").digest_size == 32


def test_problem_and_exercise_numbers():
    p, g = 47, 2
    assert pow(g, 23, p) == 1 and g != 1
    A, B = pow(g, 5, p), pow(g, 9, p)
    assert (A, B, pow(B, 5, p), pow(A, 9, p)) == (32, 42, 24, 24)
    assert [x for x in range(1, 23) if pow(g, x, p) == A] == [5]
    q = 12161315482320826121  # the subgroup order printed by dh.py
    assert (
        round(1.5 * math.sqrt(q) / 1e9, 1) == 5.2 and round(2 * math.sqrt(q) / 1e9) == 7
    )
    m = math.isqrt(1_000_003 - 1) + 1  # exercise 4
    assert (m, m, 2 * m - 1) == (1001, 1001, 2001)
    assert math.isqrt(2**36) == 2**18 and math.isqrt(2**64) == 2**32
    assert 2**32 * 16 == 64 * 2**30  # 64 GiB at 16 bytes per entry
