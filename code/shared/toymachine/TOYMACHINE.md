# The toy machine (frozen 2026-11-19)

The series' small computer. Book 1 (grade 7, `how-a-processor-runs-a-program`)
traces it by hand, Book 2 (grade 11, `von-neumann-machine`) uses its whole
instruction set, and the grade-11 project rebuilds an assembler and a simulator
for it. The university books move to a RISC-V subset (`code/shared/rv/`).

**Frozen:** printed outputs depend on these bytes. Wrap or extend in your own
chapter code; never edit this package. Report a defect to the main session.

## The machine

- **Memory:** 256 cells, addresses 0–255. Each cell holds one byte, a whole
  number from 0 to 255. Program and data share the memory (von Neumann).
- **Registers:** four general registers `R0`–`R3`, each one byte; the program
  counter `PC` (the address of the next instruction); the stack pointer `SP`,
  which starts at 0 so that the first `PUSH` writes cell 255 (the stack grows
  downward); three flags.
- **Flags**, set by every arithmetic, logic, shift and `CMP` instruction:
  - `Z` (zero): the 8-bit result is 0;
  - `N` (negative): bit 7 of the result is 1 (the result read in two's
    complement is negative);
  - `C` (carry): `ADD`/`ADDI` carried out of bit 7; `SUB`/`CMP` needed a
    borrow (the first operand, read unsigned, was smaller); `SHL`/`SHR` the
    bit shifted out; `AND`/`OR`/`XOR`/`NOT` clear it.
- **Arithmetic** wraps modulo 256: 250 + 10 = 4 with `C` = 1.
- **Input and output:** `IN` reads one whole number per line from standard
  input (0–255; a negative number −128…−1 is stored in two's complement);
  `OUT` prints a register's value as an unsigned decimal number on its own line.
- The machine starts with every register, flag and cell at 0 except the
  program loaded from address 0, and `PC` = 0. It stops at `HALT`.

## Instructions

Every instruction is **two bytes**: the first holds the operation code in
its top six bits and a register number `r` (0–3) in its bottom two
(`byte0 = 4 × opcode + r`); the second is the operand: an address, a number,
or a second register `s` (0–3). Unused fields are 0.

| Opcode | Assembly | Effect | Flags |
|---:|---|---|---|
| 0 | `HALT` | stop | — |
| 1 | `LOADI r, n` | r ← n | — |
| 2 | `LOAD r, [a]` | r ← M[a] | — |
| 3 | `STORE r, [a]` | M[a] ← r | — |
| 4 | `ADD r, s` | r ← r + s | Z N C |
| 5 | `SUB r, s` | r ← r − s | Z N C |
| 6 | `ADDI r, n` | r ← r + n | Z N C |
| 7 | `AND r, s` | r ← r AND s (bitwise) | Z N, C=0 |
| 8 | `OR r, s` | r ← r OR s | Z N, C=0 |
| 9 | `XOR r, s` | r ← r XOR s | Z N, C=0 |
| 10 | `NOT r` | r ← NOT r (flip every bit) | Z N, C=0 |
| 11 | `SHL r` | shift left one bit (bit 7 → C) | Z N C |
| 12 | `SHR r` | shift right one bit, 0 enters bit 7 (bit 0 → C) | Z N C |
| 13 | `CMP r, s` | compute r − s, set the flags, keep r | Z N C |
| 14 | `JMP a` | PC ← a | — |
| 15 | `JZ a` | if Z: PC ← a | — |
| 16 | `JNZ a` | if not Z: PC ← a | — |
| 17 | `JN a` | if N: PC ← a | — |
| 18 | `JC a` | if C: PC ← a | — |
| 19 | `IN r` | r ← next number read | — |
| 20 | `OUT r` | print r | — |
| 21 | `LOADR r, s` | r ← M[s] (address in a register) | — |
| 22 | `STORER r, s` | M[s] ← r | — |
| 23 | `PUSH r` | SP ← SP − 1; M[SP] ← r | — |
| 24 | `POP r` | r ← M[SP]; SP ← SP + 1 | — |
| 25 | `CALL a` | push PC (already the next instruction); PC ← a | — |
| 26 | `RET` | pop into PC | — |
| 27 | `NOP` | nothing | — |

Each step: **fetch** the two bytes at `PC` and `PC+1`, add 2 to `PC`,
**decode**, **execute**. A jump overwrites `PC` after the increment.

## Assembly language

```
; sum.toy -- reads n, prints 1 + 2 + ... + n
        IN    R0          ; R0 = n
        LOADI R1, 0       ; R1 = running total
        LOADI R2, 1       ; R2 = the constant 1
loop:   ADD   R1, R0      ; total = total + n
        SUB   R0, R2      ; n = n - 1 (sets Z when n reaches 0)
        JNZ   loop
        OUT   R1
        HALT
```

- One instruction per line; `;` starts a comment; case does not matter in
  mnemonics and register names.
- A **label** is a name followed by `:` at the start of a line; it stands for
  the address of what follows.
- Numbers: decimal (`42`, `-3` for 253), hexadecimal (`0x2A`), binary
  (`0b101010`), or a character in single quotes (`'A'` = 65).
- `[a]` (an address, a number or a label in brackets) for `LOAD` and `STORE`;
  a bare label or number for jumps and `CALL`.
- `DATA n, n, ...` places bytes in memory at that point (after `HALT`, with a
  label in front, it is how a program keeps an array).

## Tools (`python -m toymachine ...`, from `code/shared/toymachine/`)

| Command | Prints |
|---|---|
| `run prog.toy` | what the program outputs; reads `IN` values from standard input |
| `run --trace prog.toy` | before each step, a table row: step, PC, the instruction, R0–R3, Z N C |
| `run --dump prog.toy` | after `HALT`, the registers, flags and the non-zero memory cells |
| `asm prog.toy` | the machine code: address, the two bytes in decimal and binary, the source line |
| `dis prog.bin` | the assembly of a machine-code file (one byte per line, decimal) |

`run` stops with an error after 10 000 steps (`--steps N` changes it), so a
program that never halts is reported, not run forever. Errors (an unknown
mnemonic, a label used but not defined, a number out of range, `PC` past
255) print the line number and stop.

In Python: `from toymachine import assemble, Machine` —
`code = assemble(text)` returns a list of 256 bytes;
`m = Machine(code, inputs=[5]); m.run()`; `m.outputs`, `m.reg`, `m.mem`,
`m.flags`, `m.pc`, `m.steps`; `m.step()` executes one instruction.
