import importlib.util
import io
import random
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))
sys.path.insert(0, str(Path(__file__).parents[4] / "code" / "shared" / "toymachine"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_adders_exhaustive():
    fa = load("listings", "full_adder")
    rp = load("listings", "ripple")
    sb = load("listings", "subtract")
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                s, carry = fa.full_adder(a, b, c)
                assert 2 * carry + s == a + b + c
    for x in range(0, 256, 3):
        for y in range(0, 256, 5):
            bits, carries = rp.add_bits(rp.to_bits(x, 8), rp.to_bits(y, 8))
            assert rp.from_bits(bits) == (x + y) % 256
            assert carries[8] == int(x + y > 255)
            bits, carries = sb.sub_bits(rp.to_bits(x, 8), rp.to_bits(y, 8))
            assert rp.from_bits(bits) == (x - y) % 256 and carries[8] == int(x >= y)


def test_mux_decoder():
    m = load("listings", "mux")
    ex = load("exercises", "circuits")
    for k in range(4):
        x = [int(i == k) for i in range(4)]
        assert m.mux4(k >> 1, k & 1, x) == 1 and ex.mux4(k, x) == 1
        assert m.decoder2(k >> 1, k & 1) == x


def test_alu_against_reference_and_toy_machine():
    from toymachine import Machine, assemble

    alu = load("listings", "alu")
    rp = load("listings", "ripple")
    ex = load("exercises", "circuits")
    rng = random.Random(11)
    pairs = [(rng.randrange(256), rng.randrange(256)) for _ in range(300)]
    pairs += [(0, 0), (255, 1), (5, 5), (5, 10), (128, 128)]
    for op in ("AND", "OR", "ADD", "SUB"):
        code = assemble(f"{op} R0, R1\nHALT\n")
        for x, y in pairs:
            bits, flags = alu.alu(op, rp.to_bits(x, 8), rp.to_bits(y, 8))
            assert (rp.from_bits(bits), flags) == ex.alu_reference(op, x, y)
            m = Machine(code)
            m.reg[0], m.reg[1] = x, y
            m.run()
            assert m.reg[0] == rp.from_bits(bits) and m.flags == flags


def test_exercises():
    ex = load("exercises", "circuits")
    rp = load("listings", "ripple")
    for a in (0, 1):
        for b in (0, 1):
            assert ex.half_adder_no_xor(a, b) == ((a + b) % 2, a & b)
    wrong = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)
             if ex.full_adder_buggy(a, b, c) != ((a + b + c) % 2, (a + b + c) // 2)]
    assert len(wrong) == 6 and (0, 0, 0) not in wrong and (0, 0, 1) not in wrong
    bits, _ = ex.sub_bits_buggy(rp.to_bits(100, 8), rp.to_bits(27, 8))
    assert rp.from_bits(bits) == 72
    assert [ex.comparator(*p) for p in [(3, 9), (9, 9), (200, 7)]] == ["<", "=", ">"]


def test_latch_and_counts():
    latch = load("listings", "latch")
    assert latch.settle(0, 0, 0, 0)[1] is False
    assert latch.settle(1, 0, 0, 1) == ([(0, 1), (0, 0), (1, 0)], True)
    gc = load("listings", "gate_count")
    assert gc.measure(gc.ripple, 64) == (320, 129)
    assert gc.measure(gc.carry_select, 64) == (580, 68)
