import subprocess
import sys
from pathlib import Path

import pytest

from toymachine import Machine, ToyError, assemble, assemble_lines, disassemble

HERE = Path(__file__).resolve().parent.parent

SUM = """
; sum.toy -- reads n, prints 1 + 2 + ... + n
        IN    R0          ; R0 = n
        LOADI R1, 0       ; R1 = running total
        LOADI R2, 1       ; R2 = the constant 1
loop:   ADD   R1, R0      ; total = total + n
        SUB   R0, R2      ; n = n - 1 (sets Z when n reaches 0)
        JNZ   loop
        OUT   R1
        HALT
"""


def run(text, inputs=()):
    m = Machine(assemble(text), inputs=inputs)
    m.run()
    return m


def test_sum_example_of_the_spec():
    assert run(SUM, [10]).outputs == [55]
    assert run(SUM, [22]).outputs == [253]


def test_encoding_is_four_times_opcode_plus_register():
    rows = assemble_lines("LOADI R1, 7\nADD R3, R2\nJMP 0\nHALT")
    assert [bs for _a, bs, _n, _s in rows] == [[4 * 1 + 1, 7], [4 * 4 + 3, 2], [4 * 14, 0], [0, 0]]


def test_wraparound_and_flags():
    m = run("LOADI R0, 250\nADDI R0, 10\nHALT")
    assert m.reg[0] == 4 and m.flags == {"Z": 0, "N": 0, "C": 1}
    m = run("LOADI R0, 3\nLOADI R1, 5\nSUB R0, R1\nHALT")
    assert m.reg[0] == 254 and m.flags == {"Z": 0, "N": 1, "C": 1}
    m = run("LOADI R0, 5\nLOADI R1, 5\nCMP R0, R1\nHALT")
    assert m.reg[0] == 5 and m.flags["Z"] == 1 and m.flags["C"] == 0


def test_shifts_and_logic():
    m = run("LOADI R0, 0b10000001\nSHL R0\nHALT")
    assert m.reg[0] == 2 and m.flags["C"] == 1
    m = run("LOADI R0, 0b00000011\nSHR R0\nHALT")
    assert m.reg[0] == 1 and m.flags["C"] == 1
    m = run("LOADI R0, 0x0F\nNOT R0\nHALT")
    assert m.reg[0] == 0xF0 and m.flags["N"] == 1


def test_memory_data_and_indirect_access():
    prog = """
        LOADI R0, table    ; R0 = address of the first element
        LOADI R1, 0        ; R1 = total
        LOADI R2, 4        ; R2 = elements left
        LOADI R3, 1
loop:   PUSH  R0
        LOADR R0, R0       ; R0 = the element
        ADD   R1, R0
        POP   R0
        ADD   R0, R3       ; next address
        SUB   R2, R3
        JNZ   loop
        OUT   R1
        HALT
table:  DATA 3, 5, 7, 9
"""
    assert run(prog).outputs == [24]
    m = run("LOAD R0, [x]\nADDI R0, 1\nSTORE R0, [x]\nHALT\nx: DATA 41")
    assert m.mem[8] == 42


def test_stack_and_call():
    prog = """
        LOADI R0, 6
        CALL double
        OUT R0
        HALT
double: ADD R0, R0
        RET
"""
    m = run(prog)
    assert m.outputs == [12] and m.sp == 0
    m = run("LOADI R0, 7\nPUSH R0\nLOADI R0, 0\nPOP R1\nHALT")
    assert m.reg[1] == 7 and m.mem[255] == 7


def test_negative_numbers_and_characters():
    assert assemble("LOADI R0, -3")[1] == 253
    assert assemble("LOADI R0, 'A'")[1] == 65
    m = Machine(assemble("IN R0\nOUT R0\nHALT"), inputs=[-1])
    m.run()
    assert m.outputs == [255]


@pytest.mark.parametrize("text,msg", [
    ("FOO R0", "unknown instruction"),
    ("JMP nowhere", "not defined"),
    ("LOADI R0, 300", "does not fit"),
    ("LOADI R4, 1", "not a register"),
    ("ADD R0", "takes 2 operand"),
    ("LOAD R0, 5", "in brackets"),
    ("a: NOP\na: NOP", "defined twice"),
])
def test_assembly_errors(text, msg):
    with pytest.raises(ToyError, match=msg):
        assemble(text)


def test_runaway_program_is_stopped():
    with pytest.raises(ToyError, match="no HALT after 50 steps"):
        Machine(assemble("loop: JMP loop")).run(max_steps=50)


def test_disassemble_round_trip():
    text = "LOADI R1, 7\nLOAD R2, [9]\nADD R3, R2\nNOT R0\nJNZ 4\nRET\nHALT"
    mem = assemble(text)
    got = [disassemble(mem[i], mem[i + 1]) for i in range(0, 14, 2)]
    assert got == ["LOADI R1, 7", "LOAD R2, [9]", "ADD R3, R2", "NOT R0", "JNZ 4", "RET", "HALT"]


def test_command_line(tmp_path):
    f = tmp_path / "sum.toy"
    f.write_text(SUM)
    env_cmd = [sys.executable, "-m", "toymachine"]
    out = subprocess.run(env_cmd + ["run", str(f)], input="4\n", capture_output=True, text=True,
                         cwd=HERE, check=True).stdout
    assert out == "10\n"
    tr = subprocess.run(env_cmd + ["run", "--trace", str(f)], input="2\n", capture_output=True,
                        text=True, cwd=HERE, check=True).stdout.splitlines()
    assert tr[0].split()[:3] == ["step", "PC", "instruction"]
    assert tr[1].split()[:4] == ["1", "0", "IN", "R0"]
    assert tr[-1] == "halted after 11 steps"
    asm = subprocess.run(env_cmd + ["asm", str(f)], capture_output=True, text=True, cwd=HERE,
                         check=True).stdout.splitlines()
    assert asm[0].split()[:5] == ["0:", "76", "0", "01001100", "00000000"]
