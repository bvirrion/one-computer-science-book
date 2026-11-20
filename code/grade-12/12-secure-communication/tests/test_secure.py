import importlib.util
import io
import random
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_rsa_round_trip_and_signatures():
    rsa = load("listings", "mini_rsa")
    public, private = rsa.make_keys(61, 53, 17)
    assert private == (3233, 2753)
    assert all(rsa.apply(private, rsa.apply(public, m)) == m for m in range(3233))
    assert rsa.apply(public, 123) == 855
    rng = random.Random(1)
    for _ in range(50):
        msg = str(rng.random())
        assert rsa.verify(public, msg, rsa.sign(private, msg))


def test_diffie_hellman_agrees():
    ex = load("exercises", "sc_ex")
    rng = random.Random(2)
    for p, g in [(23, 5), (1021, 10), (2**61 - 1, 3)]:
        for _ in range(20):
            a, b = rng.randrange(2, p - 1), rng.randrange(2, p - 1)
            assert ex.dh_shared(p, a, pow(g, b, p)) == ex.dh_shared(p, b, pow(g, a, p))
    assert pow(5, 6, 23) == 8


def test_exercises():
    ex = load("exercises", "sc_ex")
    assert ex.xor_bytes(bytes([0b10110010]), bytes([0b01100111])) == bytes([0b11010101])
    m = b"Meet at the bridge at noon"
    c1, c2 = ex.encrypt_with_nonce(1, 1, m), ex.encrypt_with_nonce(1, 2, m)
    assert c1 != c2 and ex.encrypt_with_nonce(1, 1, c1) == m
    rsa = load("listings", "mini_rsa")
    public, private = rsa.make_keys(61, 53, 17)
    s = rsa.sign(private, "Pay Bea 20")
    assert ex.verify_right(public, "Pay Bea 20", s)
    assert not ex.verify_wrong(public, "Pay Bea 20", s)
    enc = ex.encrypt_text(public, "noon")
    assert enc[1] == enc[2] and enc[0] == enc[3]
    stored = ex.store_password("tulip7", rounds=1000)
    assert ex.check_password(stored, "tulip7") and not ex.check_password(stored, "tulip8")
    (a1, m1), (b1, m2) = ex.mitm(23, 5, 6, 15, 9)
    assert a1 == m1 and b1 == m2


def test_brute_force_and_chain():
    bd = load("listings", "brute_dlog")
    p = 1021
    g = bd.generator(p)
    assert len({pow(g, k, p) for k in range(1, p)}) == p - 1
    assert bd.brute_force(p, g, pow(g, 500, p)) == (500, 499)
    tc = load("listings", "toy_certificate")
    assert tc.check_chain(tc.site_cert, tc.mid_cert, tc.root_pub)
    other_root, _ = load("listings", "mini_rsa").make_keys(5003, 5009, 65537)
    assert not tc.check_chain(tc.site_cert, tc.mid_cert, other_root)


def test_problem_numbers():
    import math
    assert [pow(5, k, 23) for k in range(1, 23)].count(1) == 1
    assert len({pow(5, k, 23) for k in range(1, 23)}) == 22
    assert len({pow(2, k, 23) for k in range(1, 23)}) == 11
    assert pow(5, 5, 23) == 20 and pow(5, 12, 23) == 18
    assert pow(18, 5, 23) == pow(20, 12, 23) == 3
    assert next(k for k in range(1, 23) if pow(5, k, 23) == 20) == 5
    year = 365.25 * 24 * 3600
    assert round(2**60 / 1e9 / year, 1) == 36.5
    exponent = 2047 * math.log10(2) - 9 - math.log10(year)
    assert int(exponent) == 599 and round(10 ** (exponent - 599), 1) == 5.1
