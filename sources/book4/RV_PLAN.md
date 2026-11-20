# `code/shared/rv/` --- design note (Book 4, Phase A, 2026-11-20)

Plan for the series' RISC-V package, written by Book 4 in its first stint after
the sync, frozen when its tests pass (`FROZEN 2026-11-.. (Book 4)` as the first
line of `RV.md`). This note is the proposal; `RV.md` will be the specification
of record. Every ISA fact (formats, opcodes, funct fields, division results,
register names) gets a ledger row from the RISC-V specification and the psABI
when `RV.md` is written.

## Users

| User | Needs |
|---|---|
| Book 4 ch. 10 | `run`, `--trace`, `--regs`, `asm` (with fields), `dis`; errors that teach (misaligned access, a fault at address 0) |
| Book 4 ch. 11 | the Python API's per-step record: registers read and written, load or store, branch outcome |
| Book 4 ch. 12 | the per-step record's memory address and size, and the PC (instruction fetch) |
| Book 4 exercises | `rv` run from pytest on many inputs |
| Book 5 ch. 7--9 (code generation, optimisation, memory management) | a stable calling convention, an entry point, a heap, printing, an exit code, instruction counts (`--stats`) to measure optimisations, an assembler that accepts what a code generator writes |
| Book 2 g11 project | nothing (it uses the toy machine) |

## The subset

- **RV32I**, user-level: `lui auipc jal jalr beq bne blt bge bltu bgeu lb lh lw
  lbu lhu sb sh sw addi slti sltiu xori ori andi slli srli srai add sub sll slt
  sltu xor srl sra or and ecall ebreak`. Real encodings (R, I, S, B, U, J
  formats), checked against the specification's tables.
- **RV32M:** `mul mulh mulhsu mulhu div divu rem remu`, with the
  specification's results for division by zero (quotient all ones, remainder
  the dividend) and for overflow ($-2^{31} / -1 = -2^{31}$, remainder 0).
- **Left out:** `fence`, `fence.i`, CSR instructions, privileged
  instructions, the A, F, D and C extensions. An encoding outside the subset is
  an illegal-instruction fault.
- **Registers:** `x0`--`x31` and the ABI names (`zero ra sp gp tp t0-t6
  s0/fp s1-s11 a0-a7`), 32-bit, `x0` hard-wired to zero. Values are kept
  unsigned in Python and read signed where an instruction says so.

## Memory

- 32-bit addresses, little-endian, byte-addressed, stored sparsely in 4 KiB
  pages created on first touch inside the mapped regions only.
- **Map** (constants in `RV.md`, printed in ch. 10's figure):
  - text from `0x00010000`, **read-only** (a store there is a fault; no
    self-modifying code, which lets the simulator pre-decode the text);
  - data from `0x10000000`, in the order of the `.data` directives;
  - heap from the first 16-byte boundary after the data, grown by `sbrk`
    (ecall 9, proposed), capped at 16 MiB;
  - stack: `sp` starts at `0x7ffffff0` (16-byte aligned), region of 8 MiB
    below it;
  - everything else, address 0 included, is unmapped: an access is a fault
    naming the address, the PC and the source line.
- **Alignment:** a misaligned load or store is a fault (the specification
  allows an implementation to trap; the book's machine does, so alignment can
  be taught). A jump to an address that is not a multiple of 4 is a fault.

## Starting and stopping

- Execution starts at the label `main` if the program defines it, otherwise at
  the first address of `.text`. `ra` starts at a sentinel return address:
  `ret` from `main` ends the program with exit status `a0 & 0xff`, as in C.
  `sp` as above, `gp` and `tp` zero, every other register zero.
- **ecall services** (number in `a7`, the convention of the common teaching
  simulators, fixed here as the book's own):

  | `a7` | Service | Effect |
  |---:|---|---|
  | 1 | print integer | prints `a0` as a signed decimal, no newline |
  | 4 | print string | prints the zero-terminated bytes at address `a0` (UTF-8) |
  | 5 | read integer | reads one line from standard input, a signed decimal, into `a0`; echoes the line when input is not a terminal (as `tools/echo_input.py` does for Python), so a captured session reads as on a terminal; end of input is an error |
  | 9 | sbrk (**proposed**) | grows the heap by `a0` bytes (multiple of 4 enforced by rounding up), returns the old break in `a0` |
  | 10 | exit | exit status 0 |
  | 11 | print character | prints the byte `a0 & 0xff` |
  | 93 | exit with code | exit status `a0 & 0xff` |

  Any other number is an error naming it. `ebreak` stops the program with a
  message and, under `--regs`, the register dump.
- **Exit statuses of `python -m rv`:** the program's own status; 1 for a
  runtime fault or the step limit; 2 for an assembly error or bad usage.
  Error messages go to standard error (the capture merges them), one line:
  `rv: line 12: lw a0, 0(a1): load access fault at 0x00000000`.
- **Step limit:** 1,000,000 by default, `--steps N` to change it; reaching it
  is an error (a program that never stops is reported, not run forever).

## Assembly language

- One statement per line; `#` starts a comment; labels `name:` at the start of
  a line (several allowed), names matching `[A-Za-z_.$][A-Za-z0-9_.$]*` (so a
  code generator's `.L3:` works; directive names are reserved).
- Operands: registers by `xN` or ABI name; immediates in decimal, `0x`
  hexadecimal, `0b` binary or a character in single quotes; memory operands
  `offset(reg)`; branch and jump targets by label (or a number, as an offset).
- **Directives:** `.text .data .globl .word .half .byte .asciz .space .align`
  (`.align n` aligns to $2^n$ bytes, as GNU's assembler does for RISC-V);
  `.word` accepts labels, so jump tables work.
- **Pseudo-instructions** (the list in `styles/onecs.sty`'s `RVAsm`): `li`
  (`addi` when the value fits 12 signed bits, else `lui` + `addi` with the
  rounding term, or `lui` alone), `la` (`auipc` + `addi`, PC-relative, as GNU
  does), `mv`, `j`, `jr`, `ret`, `call` (**the book's choice:** `jal ra,
  label`, one instruction; GNU emits `auipc`+`jalr` for a call it cannot prove
  near --- said in `RV.md` and in ch. 10), `nop`, `neg`, `not`, `beqz`,
  `bnez`, `bgt`, `ble`, `seqz`, `snez`; plus the one-operand forms `jal
  label` and `jalr rs`. **Proposed additions** for code generators and
  exercises: `bgez bltz blez bgtz bgtu bleu tail` (see the report: they would
  need appending to `RVAsm`'s keyword list for highlighting).
- Two passes; every pseudo-instruction has a size known in pass 1 (`li` takes
  a number only; `la` always two words). Errors: unknown mnemonic, wrong
  operand count or kind, unknown register, immediate or offset out of range,
  undefined or duplicate label, a directive in the wrong section, a string
  without its closing quote --- each with its line number and the line.

## Command line (`python -m rv ...`, from `code/shared/rv/`)

Options may come after the file name (the capture tool appends `args=` after
it).

| Command | Prints |
|---|---|
| `run prog.S` | what the program prints |
| `run prog.S --trace` | one line per executed instruction, before the program's own output of that step: `step  pc  word  instruction  effect`, e.g. `    3  00010008  00a50533  add a0, a0, a0       a0 = 14`; stores `mem[0x7fffffec] = 5 (word)`; branches `taken -> 00010020` or `not taken`; ecalls name their service |
| `run prog.S --regs` | after the end: the 32 registers (ABI name, hex, signed decimal), the PC, the step count |
| `run prog.S --stats` | after the end: instructions executed, and by class (ALU, multiply/divide, load, store, branch taken, branch not taken, jump, ecall) |
| `run prog.S --steps N` | the step limit |
| `asm prog.S` | the assembled listing: address, word in hex, the source line; a pseudo-instruction's expansion on one line per word; then the data section in hex with its labels |
| `asm prog.S --fields` | the same with each word split into its format's fields in binary, and the format named |
| `dis words.hex [--base ADDR]` | the assembly of a file of hex words, one per line (`#` comments allowed), branch targets as addresses |

Output is deterministic: no timing, no addresses from the host.

## Python API

```python
from rv import assemble, Machine, decode, encode, disassemble, run_source, AsmError, RVFault
prog = assemble(text, name="prog.S")      # Program: words, data, symbols, entry, line map
m = Machine(prog, inputs=[5])            # or stdin=<file>; out=<file-like> (default: collect)
code = m.run(max_steps=1_000_000)        # exit status
s = m.step()                             # one instruction, returns a Step record
# Step: pc, word, text, rd, rd_value, srcs (registers read), mem_kind ('load'|'store'|None),
#       mem_addr, mem_size, branch_taken (True|False|None), next_pc, ecall (service or None)
m.x[10], m.pc, m.steps, m.output, m.exit_code, m.stats
out, code, stats = run_source(text, inputs=[...])   # for tests (Book 4 exercises, Book 5)
```

`decode(word)` returns an instruction record (format, mnemonic, fields,
immediate), `encode` the reverse, `disassemble(word, pc=None, symbols=None)`
the canonical text (ABI names, decimal immediates).

## Implementation

- One package `code/shared/rv/rv/` (`__init__.py`, `isa.py` tables,
  `asm.py`, `decode.py`, `machine.py`, `__main__.py`), standard library only,
  ruff-clean, typed where it helps reading. Text pre-decoded at load (it is
  read-only), so a step is a table dispatch: target several hundred thousand
  steps per second, enough for Book 5's test programs.
- `RV.md`: the specification of record (subset, encodings table, map,
  services, assembler syntax, CLI formats with an example each, API), in the
  style of `TOYMACHINE.md`.

## Tests (`code/shared/rv/tests/`)

- **Encodings:** golden words for every instruction (computed by hand from the
  specification's tables and cross-checked with the specification's printed
  examples, e.g. `addi x0, x0, 0` = `0x00000013`, `ecall` = `0x00000073`);
  every B and J immediate bit position; boundary immediates (±2048, ±4 KiB,
  ±1 MiB).
- **Round trip:** for every instruction and random operands (hypothesis),
  `encode → decode → disassemble → assemble` gives the same word.
- **Semantics:** every instruction against a Python reference on edge values
  (shifts by the low five bits, `sra` sign, `slt` vs `sltu`, `sltiu`'s
  sign-extended immediate compared unsigned, sign and zero extension of loads,
  `jalr` clearing bit 0, writes to `x0` ignored, the division special cases,
  `mulh*` on extreme values).
- **Pseudo-instructions:** `li` on 0, ±1, 2047, 2048, −2048, −2049,
  0x7ffff800, 0x80000000, 0xffffffff and random values; `la` across regions.
- **Programs:** factorial (recursive, under the convention), string printing,
  `read_int` from standard input, a jump table, `sbrk`, `ret` from `main`
  with a status.
- **Errors:** each assembly error and each fault message, with its line.
- **CLI:** golden outputs for `--trace`, `--regs`, `--stats`, `asm`,
  `asm --fields`, `dis` on small programs; determinism (two runs, same bytes).
- No external RISC-V tool is installed (binutils here targets x86 only), so the
  encodings rest on the specification's tables and the hand-checked goldens;
  `RV.md` says so.

## Questions for the sync

1. **`sbrk` (ecall 9):** the run file lists printing an integer, a string, a
   character, reading an integer and exiting. Book 5's memory-management and
   code-generation chapters will want a heap. Add it now (before the freeze)?
2. **A capture directive for `asm`/`dis`:** `tools/capture_output.py` always
   runs `python -m rv run`. A directive such as `# capture: rv=asm` (or
   `rv=dis`) would let ch. 10 print encodings without a shell wrapper whose
   command line shows instead.
3. **`RVAsm` highlighting:** append `mulhsu mulhu bgez bltz blez bgtz bgtu bleu
   tail` to the keyword list (append-only, a `% Book 4:` line), if the extra
   pseudo-instructions are accepted.
4. **`call` as one `jal`:** accepted, or should `call` follow GNU (`auipc` +
   `jalr`, two words)?
