"""The single-cycle model agrees with rv at every step of every program of the chapter."""
from pathlib import Path

import pytest
from datapath import CONTROL, check, imm_gen
from datapath_more import cycle_more
from rv import assemble

HERE = Path(__file__).resolve().parent.parent
PROGRAMS = sorted((HERE / "listings").glob("*.S")) + sorted((HERE / "exercises").glob("*.S"))
EXTRA = """
main:   li   t0, 0x12345678       # lui + addi
        li   t1, -2048
        lui  t2, 0xfffff
        call f                    # jal
        addi a0, a0, 1
        la   t3, g
        jalr ra, 0(t3)            # jalr through a register
        li   a0, 0
        li   a7, 93
        ecall
f:      addi a0, zero, 41
        ret
g:      slt  t4, t1, t0
        sra  t5, t1, t4
        sub  t6, t0, t1
        xori s1, t6, -1
        ret
"""


@pytest.mark.parametrize("path", PROGRAMS, ids=lambda p: p.name)
def test_agrees_with_rv(path):
    agree, outside = check(path.read_text())
    assert agree > 0
    agree2, outside2 = check(path.read_text(), model=cycle_more)
    assert agree2 + outside2 == agree + outside and outside2 <= outside


def test_lui_jal_jalr():
    agree, outside = check(EXTRA)
    agree2, outside2 = check(EXTRA, model=cycle_more)
    assert outside2 == 2 and outside > outside2  # only auipc (from la) and the ecall remain


def test_immediates_match_assembler():
    prog = assemble("main: addi a0, a0, -1\n sw ra, 12(sp)\n beq a0, zero, main\n"
                    " lw t0, -20(s0)\n bne a0, zero, main\n sw t1, -2048(sp)\n")
    assert [imm_gen(w) for w in prog.words] == [-1, 12, -8, -20, -16, -2048]


def test_control_table():
    lw, sw = CONTROL[0b0000011], CONTROL[0b0100011]
    assert (lw.mem_read, lw.mem_to_reg, lw.reg_write) == (1, 1, 1)
    assert (sw.mem_write, sw.reg_write) == (1, 0)
    assert all(c.reg_write == 0 for c in CONTROL.values() if c.branch or c.mem_write)
