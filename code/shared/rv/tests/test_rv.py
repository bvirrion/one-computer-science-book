import subprocess
import sys
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from rv import (EXIT_ADDR, SP_START, TEXT_BASE, AsmError, EncodingError, Machine, RVFault, StepLimit,
                assemble, decode, disassemble, encode, run_source)
from rv.isa import MASK, SPEC

ROOT = Path(__file__).resolve().parent.parent

# Golden words, checked against the specification's field layouts (and the words GNU as prints for the
# same lines: addi sp,sp,-16 = ff010113, sw ra,12(sp) = 00112623, ret = 00008067).
GOLDEN = [
    ("addi x0, x0, 0", 0x00000013),
    ("nop", 0x00000013),
    ("ecall", 0x00000073),
    ("ebreak", 0x00100073),
    ("add a0, a0, a0", 0x00A50533),
    ("addi sp, sp, -16", 0xFF010113),
    ("sw ra, 12(sp)", 0x00112623),
    ("lw ra, 12(sp)", 0x00C12083),
    ("ret", 0x00008067),
    ("addi a0, zero, 1", 0x00100513),
    ("lui a0, 0x12345", 0x12345537),
    ("sub t0, t1, t2", 0x407302B3),
    ("srai a0, a0, 3", 0x40355513),
    ("mul a0, a0, a1", 0x02B50533),
    ("divu a0, a1, a2", 0x02C5D533),
    ("lbu t0, -1(a0)", 0xFFF54283),
    ("sb t0, -1(a0)", 0xFE550FA3),
]


@pytest.mark.parametrize("line,word", GOLDEN)
def test_golden_encodings(line, word):
    assert assemble(line).words == [word]


def test_golden_branch_and_jump_offsets():
    p = assemble("start: beq a0, a1, two\n nop\ntwo: j start\n")
    assert p.words == [0x00B50463, 0x00000013, 0xFF9FF06F]


def test_call_and_tail_are_one_jal():
    p = assemble("main: call f\n tail f\nf: ret\n")
    assert len(p.words) == 3
    assert decode(p.words[0]).mnemonic == "jal" and decode(p.words[0]).rd == 1
    assert decode(p.words[1]).mnemonic == "jal" and decode(p.words[1]).rd == 0


REG = st.integers(0, 31)


@settings(max_examples=400, deadline=None)
@given(st.sampled_from(sorted(SPEC)), REG, REG, REG, st.integers(-(1 << 20), (1 << 20) - 1))
def test_encode_decode_round_trip(mn, rd, rs1, rs2, raw):
    fmt, kind = SPEC[mn][0], SPEC[mn][1]
    imm = {"I": raw % 4096 - 2048, "L": raw % 4096 - 2048, "JR": raw % 4096 - 2048, "S": raw % 4096 - 2048,
           "SH": raw % 32, "B": (raw % 4096 - 2048) * 2, "U": raw % (1 << 20),
           "J": (raw % (1 << 20) - (1 << 19)) * 2, "R": 0, "N": 0}[kind]
    w = encode(mn, rd, rs1, rs2, imm)
    ins = decode(w)
    assert ins.mnemonic == mn and ins.word == w
    if kind != "N":
        if fmt in ("R", "I", "U", "J"):
            assert ins.rd == rd
        if fmt in ("R", "I", "S", "B") and kind not in ("U",):
            assert ins.rs1 == rs1
        if fmt in ("R", "S", "B"):
            assert ins.rs2 == rs2
        if kind != "R":
            assert ins.imm == imm
    # the disassembly assembles back to the same word (branches and jumps: next test)
    if kind not in ("B", "J"):
        assert assemble(disassemble(w)).words == [w]


@settings(max_examples=200, deadline=None)
@given(st.integers(-2048, 2047).map(lambda k: k * 2))
def test_branch_text_round_trip(off):
    w = encode("bne", 0, 10, 11, off)
    assert assemble(disassemble(w, TEXT_BASE)).words == [w]
    j = encode("jal", 1, 0, 0, off * 64)
    assert assemble(disassemble(j, TEXT_BASE)).words == [j]


def test_decode_rejects_words_outside_the_subset():
    for w in (0x00000000, 0xFFFFFFFF, 0x0000000F, 0x02000033 | (7 << 25)):
        assert decode(w) is None
    assert disassemble(0) == ".word 0x00000000"


def a0_after(src, inputs=()):
    m = Machine(assemble("main:\n" + src + "\n ret\n"), inputs=list(inputs))
    m.run()
    return m.x[10]


@pytest.mark.parametrize("value", [0, 1, -1, 2047, 2048, -2048, -2049, 0x7FFFF800, 0x7FFFFFFF,
                                   0x80000000, 0xFFFFFFFF, 0x12345678, 0xFFFFF800, 0x00001000])
def test_li_edge_values(value):
    p = assemble(f"li a0, {value}")
    m = Machine(p)
    for _ in p.words:
        m.step()
    assert m.x[10] == value & MASK
    expected = 1 if -2048 <= (value if value < 1 << 31 else value - (1 << 32)) <= 2047 else \
        (1 if value & 0xFFF == 0 else 2)
    assert len(p.words) == expected


def test_li_out_of_range():
    with pytest.raises(AsmError, match="does not fit"):
        assemble("li a0, 0x100000000")


SEMANTICS = [
    ("li t0, 7\nli t1, -2\ndiv a0, t0, t1", -3),
    ("li t0, 7\nli t1, -2\nrem a0, t0, t1", 1),
    ("li t0, -7\nli t1, 2\nrem a0, t0, t1", -1),
    ("li t0, 7\ndiv a0, t0, zero", -1),
    ("li t0, 7\nrem a0, t0, zero", 7),
    ("li t0, 7\ndivu a0, t0, zero", 0xFFFFFFFF),
    ("li t0, 7\nremu a0, t0, zero", 7),
    ("li t0, 0x80000000\nli t1, -1\ndiv a0, t0, t1", 0x80000000),
    ("li t0, 0x80000000\nli t1, -1\nrem a0, t0, t1", 0),
    ("li t0, -1\nli t1, -1\nmulh a0, t0, t1", 0),
    ("li t0, -1\nli t1, -1\nmulhu a0, t0, t1", 0xFFFFFFFE),
    ("li t0, -1\nli t1, -1\nmulhsu a0, t0, t1", 0xFFFFFFFF),
    ("li t0, 0x10000\nmul a0, t0, t0", 0),
    ("li t0, -8\nsrai a0, t0, 1", -4),
    ("li t0, -8\nsrli a0, t0, 28", 15),
    ("li t0, 1\nli t1, 33\nsll a0, t0, t1", 2),
    ("li t0, -1\nli t1, 1\nslt a0, t0, t1", 1),
    ("li t0, -1\nli t1, 1\nsltu a0, t0, t1", 0),
    ("li t0, -1\nsltiu a0, t0, -1", 0),
    ("li t0, 5\nsltiu a0, t0, -1", 1),
    ("li t0, 0xff\nxori a0, t0, -1", 0xFFFFFF00),
    ("li t0, 0\nseqz a0, t0", 1),
    ("li t0, 9\nsnez a0, t0", 1),
    ("li t0, 9\nneg a0, t0", -9),
    ("li t0, 9\nnot a0, t0", -10),
    ("li a0, 5\naddi zero, a0, 1\nmv a0, zero", 0),
    ("lui a0, 0xfffff\nsrai a0, a0, 12", -1),
]


@pytest.mark.parametrize("src,expected", SEMANTICS)
def test_semantics(src, expected):
    assert a0_after(src) == expected & MASK


def test_auipc_reads_its_own_address():
    p = assemble("nop\nauipc a0, 1\n")
    m = Machine(p)
    m.step()
    m.step()
    assert m.x[10] == TEXT_BASE + 4 + 0x1000


def test_loads_extend_and_stores_truncate():
    src = """
        .data
w:      .word 0x80ff7f01
        .text
main:   la t0, w
        lb a0, 3(t0)
        lbu a1, 3(t0)
        lh a2, 2(t0)
        lhu a3, 2(t0)
        li t1, 0x12345678
        sb t1, 0(t0)
        lw a4, 0(t0)
        sh t1, 2(t0)
        lw a5, 0(t0)
        ret
    """
    m = Machine(src)
    m.run()
    assert [m.x[i] for i in range(10, 16)] == [
        0xFFFFFF80, 0x80, 0xFFFF80FF, 0x80FF, 0x80FF7F78, 0x56787F78]


def test_data_directives_little_endian_and_align():
    p = assemble('.data\na: .byte 1, 2\n .align 2\nb: .half -1\nc: .asciz "hi\\n"\n .space 3\nd: .word c\n')
    assert p.symbols["b"] == p.data_base + 4
    assert p.data[:4] == bytes([1, 2, 0, 0])
    assert p.data[4:6] == b"\xff\xff"
    assert p.data[6:10] == b"hi\n\0"
    assert p.symbols["d"] == p.data_base + 13
    assert int.from_bytes(p.data[13:17], "little") == p.symbols["c"]


def test_strings_and_output():
    src = r"""
        .data
msg:    .asciz "x = "
        .text
main:   la a0, msg
        li a7, 4
        ecall
        li a0, -42
        li a7, 1
        ecall
        li a0, '\n'
        li a7, 11
        ecall
        li a0, 3
        li a7, 93
        ecall
    """
    out, code, stats = run_source(src)
    assert out == "x = -42\n" and code == 3 and stats["ecalls"] == 4


def test_read_int_and_exit():
    src = "main: li a7, 5\n ecall\n slli a0, a0, 1\n li a7, 1\n ecall\n li a7, 10\n ecall\n"
    assert run_source(src, [21])[:2] == ("42", 0)
    with pytest.raises(RVFault, match="no input left"):
        run_source(src, [])
    with pytest.raises(RVFault, match="not a number"):
        run_source(src, ["seven"])


def test_main_is_the_entry_and_ret_exits_with_a0():
    src = "helper: li a0, 99\n ret\nmain: li a0, 300\n ret\n"
    m = Machine(src)
    assert m.pc == m.prog.symbols["main"]
    assert m.x[1] == EXIT_ADDR and m.x[2] == SP_START and SP_START % 16 == 0
    assert m.run() == 300 & 0xFF


def test_no_main_starts_at_text():
    assert run_source("li a0, 4\nret\n")[1] == 4


def test_sbrk_grows_the_heap():
    src = """
main:   li a0, 10
        li a7, 9
        ecall
        mv s0, a0           # old break: the start of the heap
        li t0, 1234
        sw t0, 8(s0)        # inside the 12 bytes we got
        lw a0, 8(s0)
        li a7, 1
        ecall
        li a0, 0
        li a7, 9
        ecall               # sbrk(0): the current break
        sub a0, a0, s0
        li a7, 1
        ecall
        lw t0, 12(s0)       # past the break: faults
        ret
    """
    m = Machine(src)
    with pytest.raises(RVFault, match="load access fault"):
        m.run()
    assert m.output_text == "123412"
    assert m.mem.heap_start % 16 == 0


def test_sbrk_refuses_too_much():
    assert a0_after("li a0, 0x2000000\nli a7, 9\necall") == MASK


@pytest.mark.parametrize("src,msg", [
    ("li a0, 0\nlw a1, 0(a0)", "load access fault at 0x00000000"),
    ("li a0, 2\nsw a1, 0(sp)\naddi a0, sp, 2\nlw a1, 0(a0)", "misaligned word load"),
    ("addi a0, sp, 1\nsh a1, 0(a0)", "misaligned half store"),
    ("la a0, main\nsw a1, 0(a0)", "read-only text"),
    ("li a0, 0x10002\njr a0", "misaligned address"),
    ("li a0, 0x1000\njalr a0", "outside the program"),
    (".word 0\n", "illegal instruction 0x00000000"),
    ("li a7, 42\necall", "unknown ecall 42"),
    ("ebreak", "no debugger"),
    ("lui sp, 0x7f7ff\nsw a0, 0(sp)", "store access fault"),
])
def test_faults(src, msg):
    m = Machine("main:\n" + src + "\nret\n")
    with pytest.raises(RVFault, match=msg) as e:
        m.run()
    assert e.value.pc is not None


def test_step_limit():
    with pytest.raises(StepLimit):
        Machine("main: j main\n").run(max_steps=100)


def test_running_off_the_end_is_a_fault():
    with pytest.raises(RVFault, match="ran past the end"):
        Machine("li a0, 1\n").run()


@pytest.mark.parametrize("src,msg", [
    ("lwz a0, 0(a1)", "unknown instruction 'lwz'"),
    ("add a0, a1", "expected add rd, rs1, rs2"),
    ("addi a0, a1, 4096", "out of range"),
    ("beq a0, a1, nowhere", "undefined label 'nowhere'"),
    ("x: nop\nx: nop", "defined twice"),
    ("$x: nop", "unknown instruction"),
    ("add a0, a1, q9", "unknown register 'q9'"),
    (".data\nadd a0, a0, a0", "in the .data section"),
    (".text\n.asciz \"no\"", "belongs in .data"),
    (".data\n.asciz \"bad \\q\"", "unknown escape"),
    (".dat", "unknown directive"),
    ("slli a0, a0, 32", "shift amount"),
])
def test_assembly_errors(src, msg):
    with pytest.raises(AsmError, match=msg) as e:
        assemble(src)
    assert str(e.value).startswith("line ")


def test_labels_accept_dot_and_underscore():
    p = assemble(".L_loop.1: nop\n_x: j .L_loop.1\n")
    assert p.symbols == {".L_loop.1": TEXT_BASE, "_x": TEXT_BASE + 4}


def test_label_arithmetic_and_numeric_targets():
    p = assemble(".data\nt: .word 1, 2\n.text\nmain: la a0, t+4\n lw a0, 0(a0)\n beq zero, zero, 0x00010010\n"
                 "ret\n ret\n")
    assert Machine(p).run() == 2


def test_step_record():
    m = Machine("main: li t0, 5\n sw t0, -4(sp)\n lw t1, -4(sp)\n beq t0, t1, done\n nop\ndone: ret\n")
    s1 = m.step()
    assert (s1.kind, s1.rd, s1.rd_value, s1.srcs) == ("alu", 5, 5, ())
    s2 = m.step()
    assert (s2.kind, s2.mem_kind, s2.mem_addr, s2.mem_size, s2.mem_value, s2.rd, s2.srcs) == \
        ("store", "store", SP_START - 4, 4, 5, None, (2, 5))
    s3 = m.step()
    assert (s3.mem_kind, s3.rd, s3.rd_value, s3.srcs) == ("load", 6, 5, (2,))
    s4 = m.step()
    assert (s4.kind, s4.branch_taken, s4.next_pc, s4.text) == ("branch", True, TEXT_BASE + 20,
                                                               "beq t0, t1, done")
    s5 = m.step()
    assert (s5.kind, s5.next_pc, s5.rd) == ("jump", EXIT_ADDR, None)
    assert m.halted and m.exit_code == 0


def test_ecall_hook_and_table():
    seen = []

    def hook(m, n):
        seen.append(n)
        if n == 64:
            m.set_reg(10, 77)
            return True
        return False

    m = Machine("main: li a7, 64\n ecall\n ret\n")
    m.on_ecall = hook
    assert m.run() == 77 and seen == [64]
    m = Machine("main: li a7, 65\n ecall\n ret\n")
    m.on_ecall = hook
    with pytest.raises(RVFault, match="unknown ecall 65"):
        m.run()
    m = Machine("main: li a0, 5\n li a7, 1\n ecall\n li a0, 0\n ret\n")
    m.ecalls[1] = lambda mm: mm.write(f"<{mm.reg('a0')}>")
    m.run()
    assert m.output_text == "<5>"


def test_ebreak_hook():
    hits = []
    m = Machine("main: li a0, 1\n ebreak\n addi a0, a0, 1\n ret\n")
    m.on_ebreak = lambda mm: hits.append(mm.pc)
    assert m.run() == 2 and hits == [TEXT_BASE + 4]


def test_stats_counts():
    src = "main: li t0, 3\nloop: addi t0, t0, -1\n sw t0, -4(sp)\n lw t1, -4(sp)\n bnez t0, loop\n ret\n"
    m = Machine(src)
    m.run()
    assert m.stats == {"instructions": 14, "loads": 3, "stores": 3, "branches": 3, "taken": 2,
                       "jumps": 1, "ecalls": 0}


def test_determinism():
    src = (ROOT / "tests" / "programs" / "fact.S").read_text()
    a = run_source(src, [10])
    b = run_source(src, [10])
    assert a == b == ("10! = 3628800\n", 0, a[2])


# ---- the command line -------------------------------------------------------------------------------
def cli(*args, stdin=""):
    env = {"PYTHONPATH": str(ROOT), "PATH": "/usr/bin:/bin"}
    r = subprocess.run([sys.executable, "-m", "rv", *args], input=stdin, capture_output=True, text=True,
                       cwd=ROOT / "tests" / "programs", env=env)
    return r.returncode, r.stdout, r.stderr


@pytest.mark.parametrize("name", ["fact_run", "fact_trace", "fact_stats", "fact_asm", "fact_fields",
                                  "words_dis", "fault", "asm_error"])
def test_cli_golden(name):
    spec = (ROOT / "tests" / "golden" / f"{name}.cmd").read_text().split("\n")
    args, stdin = spec[0].split(), "\n".join(spec[1:])
    code, out, err = cli(*args, stdin=stdin)
    expected = (ROOT / "tests" / "golden" / f"{name}.txt").read_text()
    assert f"[exit {code}]\n{out}{err}" == expected


def test_cli_usage_error():
    code, _out, err = cli("run")
    assert code == 2 and "usage" in err
    code, _out, err = cli("run", "missing.S")
    assert code == 2 and err == "rv: No such file or directory: missing.S\n"


def test_encoding_error_type():
    with pytest.raises(EncodingError):
        encode("beq", 0, 1, 2, 3)


def test_precise_trap_hook():
    src = "main: li a7, 200\n ecall\n .word 0x30200073\n li a0, 7\n ret\n"
    log = []

    def monitor(m, cause):
        log.append((cause, m.pc, m.reg("a7") if cause == "ecall" else None))
        m.pc += 4

    m = Machine(src)
    m.on_trap = monitor
    assert m.run() == 7
    base = TEXT_BASE
    assert log == [("ecall", base + 4, 200), ("illegal", base + 8, None)]
    assert m.traps == 2 and m.stats["ecalls"] == 1


def test_trap_handler_that_forgets_to_advance_loops_until_the_limit():
    m = Machine("main: li a7, 200\n ecall\n ret\n")
    m.on_trap = lambda mm, cause: None
    with pytest.raises(StepLimit):
        m.run(max_steps=1000)
    assert m.traps == 999


def test_trap_record():
    m = Machine("main: ebreak\n ret\n")
    m.on_trap = lambda mm, cause: setattr(mm, "pc", mm.pc + 4)
    st = m.step()
    assert (st.kind, st.trap, st.next_pc) == ("system", "ebreak", TEXT_BASE + 4)


def test_jump_outside_by_a_handler_faults_clearly():
    m = Machine("main: ecall\n ret\n")
    m.on_trap = lambda mm, cause: setattr(mm, "pc", 0x2000)
    with pytest.raises(RVFault, match="no instruction at 0x00002000"):
        m.run()
