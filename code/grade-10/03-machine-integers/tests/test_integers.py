import importlib.util
import io
import random
import sys
from contextlib import redirect_stdout
from datetime import UTC, datetime
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "exercises"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


rng = random.Random(2026)


def test_to_base_round_trip():
    to_base = load("listings", "to_base").to_base
    for _ in range(500):
        n, b = rng.randint(0, 10**9), rng.randint(2, 36)
        assert int(to_base(n, b), b) == n
    assert to_base(255, 16) == "FF" and to_base(0, 2) == "0"


def test_twos_complement_round_trip():
    mod = load("listings", "twos")
    for n in (4, 8, 16):
        for x in range(-(2 ** (n - 1)), 2 ** (n - 1)):
            u = mod.encode(x, n)
            assert 0 <= u < 2**n and mod.decode(u, n) == x
            # negation = flip every bit and add one
            assert mod.encode(-x, n) == ((~u & (2**n - 1)) + 1) % 2**n


def test_bit_ops():
    mod = load("exercises", "bit_ops")
    for _ in range(300):
        x, i = rng.randint(0, 2**16), rng.randint(0, 15)
        assert mod.test_bit(x, i) == (format(x, "032b")[31 - i] == "1")
        assert mod.test_bit(mod.set_bit(x, i), i)
        assert not mod.test_bit(mod.clear_bit(x, i), i)
        assert mod.clear_bit(mod.set_bit(x, i), i) == mod.clear_bit(x, i)


def test_decode_bug():
    mod = load("exercises", "decode_bug")
    assert mod.decode_buggy("11111011") == 251
    assert mod.decode("11111011") == -5 and mod.decode("01111111") == 127


def test_popcount():
    mod = load("exercises", "popcount")
    for _ in range(300):
        x = rng.randint(0, 2**40)
        ones = bin(x).count("1")
        assert mod.popcount(x) == (ones, ones)
        assert mod.popcount_shift(x) == (ones, x.bit_length())


def test_add_n_bits_matches_signed_arithmetic():
    add = load("exercises", "add_n_bits").add_n_bits
    twos = load("listings", "twos")
    n = 8
    for a in range(256):
        for b in range(0, 256, 7):
            r, carry, overflow = add(a, b, n)
            assert r == (a + b) % 256 and carry == (a + b > 255)
            signed = twos.decode(a, n) + twos.decode(b, n)
            assert overflow == (not -128 <= signed <= 127)
    assert add(100, 50, 8) == (150, False, True)


def test_rollover():
    mod = load("exercises", "rollover")
    assert mod.to_date(2**31 - 1) == datetime(2038, 1, 19, 3, 14, 7, tzinfo=UTC)
    assert mod.to_date(mod.wrap_signed(2**31, 32)) == datetime(1901, 12, 13, 20, 45, 52, tzinfo=UTC)


def test_wrap_counter():
    add = load("listings", "wrap").add_unsigned
    assert add(65535, 1, 16) == 0 and add(250, 10, 8) == 4


def test_toy_machine_wraps_like_python():
    sys.path.insert(0, str(HERE.parent.parent / "shared" / "toymachine"))
    from toymachine import Machine, assemble

    m = Machine(assemble((HERE / "listings" / "toy_wrap.toy").read_text()))
    m.run()
    assert m.reg[0] == (250 + 10) % 256
