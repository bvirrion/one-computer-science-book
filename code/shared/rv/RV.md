FROZEN 2026-11-20 (Book 4)

# rv: the series' RISC-V machine

The university books' processor: a 32-bit RISC-V subset, its assembler, its disassembler and a
simulator, in plain Python (no dependencies). Book 4 (University Year 2) teaches it in
`assembly-programming` and models its pipeline and caches in the next two chapters; Book 5 compiles to
it, switches contexts on it and runs guests on its Python API. The school books and Book 3 use the toy
machine (`code/shared/toymachine/`).

**Frozen:** printed outputs depend on these bytes. Wrap or extend it in your own chapter code (the hooks
below exist for that); never edit this package. Report a defect to the main session.

## The instruction set

**RV32I** (the base integer instructions, user level) **and RV32M** (multiply and divide), encoded
exactly as the RISC-V Unprivileged ISA specifies (ledger rows `b2:rv-*` in `sources/ledger/book4.md`).
Left out: `fence`, the CSR instructions, everything privileged, and the A, F, D and C extensions. A
word outside the subset is an *illegal instruction*.

| Format | Instructions | Operands |
|---|---|---|
| R | `add sub sll slt sltu xor srl sra or and`, `mul mulh mulhsu mulhu div divu rem remu` | `rd, rs1, rs2` |
| I | `addi slti sltiu xori ori andi` | `rd, rs1, imm` (−2048…2047) |
| I | `slli srli srai` | `rd, rs1, shamt` (0…31) |
| I | `lb lh lw lbu lhu` | `rd, offset(rs1)` |
| I | `jalr` | `rd, offset(rs1)`, also `rd, rs1, imm`, and `jalr rs` (= `jalr ra, 0(rs)`) |
| I | `ecall ebreak` | none |
| S | `sb sh sw` | `rs2, offset(rs1)` |
| B | `beq bne blt bge bltu bgeu` | `rs1, rs2, target` (±4 KiB) |
| U | `lui auipc` | `rd, imm20` (0…0xfffff, the upper 20 bits) |
| J | `jal` | `rd, target` (±1 MiB), also `jal target` (= `jal ra, target`) |

Semantics as specified: `x0` reads 0 and ignores writes; arithmetic wraps modulo 2^32; `sra`/`srai`
copy the sign bit; register shifts use the low 5 bits of `rs2`; `lb`/`lh` sign-extend, `lbu`/`lhu`
zero-extend; stores keep the low byte or half; `jalr` clears bit 0 of the target. **Division**: `div` and
`rem` round toward zero; division by zero gives quotient −1 (all bits set; `divu`: 2^32 − 1) and remainder
the dividend; the overflow case −2^31 / −1 gives quotient −2^31 and remainder 0. No division traps.

A *target* is a label, `label+n`, `label-n`, or an absolute address written as a number
(`beq a0, a1, 0x00010010`, as the disassembler prints it).

**Registers:** `x0`–`x31`, or their ABI names `zero ra sp gp tp t0–t2 s0/fp s1 a0–a7 s2–s11 t3–t6`.

## Pseudo-instructions

| Pseudo | Real instructions |
|---|---|
| `li rd, n` | `addi rd, zero, n` if −2048 ≤ n ≤ 2047; else `lui rd, hi` then `addi rd, rd, lo` (just `lui` when `lo` = 0), with hi = (n + 0x800) >> 12 and lo the low 12 bits read signed. n is a number (decimal, `0x`, `0b`, a character `'A'` or `'\n'`), from −2^31 to 2^32 − 1. |
| `la rd, label` | `auipc rd, hi` then `addi rd, rd, lo` (pc-relative, always two words) |
| `mv rd, rs` | `addi rd, rs, 0` |
| `not rd, rs` / `neg rd, rs` | `xori rd, rs, -1` / `sub rd, zero, rs` |
| `seqz rd, rs` / `snez rd, rs` | `sltiu rd, rs, 1` / `sltu rd, zero, rs` |
| `nop` | `addi zero, zero, 0` (the word 0x00000013) |
| `j t` / `jr rs` / `ret` | `jal zero, t` / `jalr zero, 0(rs)` / `jalr zero, 0(ra)` |
| `call f` / `tail f` | `jal ra, f` / `jal zero, f`: **one `jal`** (see below) |
| `beqz bnez bgez bltz rs, t` | `beq bne bge blt rs, zero, t` |
| `blez bgtz rs, t` | `bge blt zero, rs, t` |
| `bgt ble bgtu bleu rs, rt, t` | `blt bge bltu bgeu rt, rs, t` (operands swapped) |

**Documented simplification: `call` and `tail`.** A real RISC-V assembler emits `call f` as `auipc ra,
hi` + `jalr ra, lo(ra)` and `tail f` as `auipc t1, hi` + `jalr zero, lo(t1)`, so that the target may be
anywhere in the 32-bit address space (ledger `b2:rv-call-tail`). rv's programs are small, so it emits
one `jal` (±1 MiB), which keeps traces and instruction counts short. A chapter that prints a `call` says
this once ("a real assembler emits two instructions, `auipc` and `jalr`, for a target that may be far").

## Assembly syntax

- One statement per line; `#` starts a comment (outside quotes). Labels `name:`, any number before a
  statement, matching `[A-Za-z_.][A-Za-z0-9_.]*` (so `.L1` and `loop_2` are labels; no `$`). Mnemonics
  are case-insensitive; labels are not. Operands are separated by commas.
- Directives: `.text`, `.data` (switch section), `.globl name` (accepted, recorded, no effect),
  `.word v, …` (32-bit; a value may be a label), `.half`, `.byte`, `.asciz "s", …` (UTF-8 bytes and a NUL;
  escapes `\n \t \r \0 \\ \" \' \xHH`), `.space n` (n zero bytes), `.align n` (to a multiple of 2^n; in
  `.text` it pads with `nop`). Data is never aligned implicitly: put `.align 2` before a `.word` that
  follows bytes. In `.text` only instructions, `.word` (a raw word, e.g. to stage an illegal instruction)
  and `.align` are allowed.
- Two passes: labels may be used before they are defined. An error stops the assembly with one message,
  e.g. `line 2: addi a0, a0, 5000: immediate 5000 out of range -2048..2047`.

## The machine

- **Memory** (little-endian, byte-addressed, 32-bit addresses), three regions; every other address
  faults (address 0 included, so a null pointer stops the program):
  - text from `0x00010000`: the instruction words, read-only (loads allowed, stores fault);
  - data from `0x10000000`: the `.data` section, then the **heap** from the next multiple of 16, which
    `sbrk` grows (at most 16 MiB) and shrinks;
  - the **stack**: 8 MiB just below `0x80000000`.
- **Alignment:** a word access needs an address that is a multiple of 4, a half a multiple of 2; a
  misaligned load or store faults (the specification lets an execution environment choose; rv chooses
  the strict one). A taken branch or a jump to an address that is not a multiple of 4, or outside the
  text, faults **at the branch or jump**, as the specification reports it.
- **Start:** `pc` = the label `main` if the program defines it in `.text`, else the first instruction.
  Every register is 0 except `sp` = `0x7ffffff0` (16-byte aligned, as the calling convention requires at
  every call) and `ra` = `0xffff0000`, the loader's exit address: a jump there (`ret` from `main`) ends the
  program with status `a0 & 0xff`. `gp` and `tp` are 0.
- **Stop:** an exit ecall, a return from `main`, or a fault. Running past the last instruction is a fault
  (`execution ran past the end of the program`): end with `ret` or an exit.

## System calls (`ecall`)

The number is in `a7`, the argument and the result in `a0`. The numbers are those of the RARS teaching
simulator, and 93 is Linux's `exit` (ledger `b2:rv-ecalls`, `b2:linux-exit-93`).

| a7 | Name | Effect |
|---:|---|---|
| 1 | print int | print `a0` as a signed decimal, no newline |
| 4 | print string | print the NUL-terminated UTF-8 string at address `a0` |
| 5 | read int | read one line of standard input, a decimal (or `0x…`) number, into `a0`; when standard input is not a terminal the line is echoed, so a transcript reads as a terminal session; end of input or a non-number is a fault |
| 9 | sbrk | move the heap's break by `a0` bytes (rounded up to a multiple of 4; negative shrinks); `a0` = the old break, or −1 if the heap would pass 16 MiB or go below its start |
| 10 | exit | stop with status 0 |
| 11 | print char | print the character `a0 & 0xff` |
| 93 | exit with code | stop with status `a0 & 0xff` |

Any other number is a fault (`unknown ecall 42 (the number is read from a7)`) unless a hook handles it;
`ebreak` is a fault (`ebreak: a breakpoint, and no debugger is attached`) unless a hook handles it.

## Command line

Run from a chapter's `listings/` with `code/shared/rv` on `PYTHONPATH` (`tools/capture_output.py` does it
for every `.S` listing; `# capture: rv=asm` or `rv=dis` selects the other two commands).

```
python -m rv run prog.S [--trace] [--regs] [--stats] [--steps N]
python -m rv asm prog.S [--fields | --hex]
python -m rv dis words.hex [--base ADDR]
```

Options may come before or after the file.

- `run`: assemble and run. Exit status: the program's own (`a0 & 0xff`), **1** for a fault or the step
  limit, **2** for an assembly error or a usage error. A fault prints one line on standard error after
  what the program printed (on a line of its own):
  `rv: line 5: lw a0, 0(a1): load access fault at 0x00000000` (line number and statement without its
  comment and labels). The step limit (default 1,000,000 instructions, `--steps N`) gives
  `rv: line 1: j main: stopped after 50 steps, the step limit (raise it with --steps N)`.
- `--trace`: a header, then one line per instruction:
  ```
   step  pc        word      instruction               effect
      1  00010000  ff010113  addi sp, sp, -16          sp = 0x7fffffe0
      2  00010004  00112623  sw ra, 12(sp)             mem[0x7fffffec] = 0xffff0000 (word)
     19  00010084  00812303  lw t1, 8(sp)              t1 = 2  <- mem[0x7fffffd8] (word)
      9  0001006c  02a35663  bge t1, a0, base          not taken
     16  0001006c  02a35663  bge t1, a0, base          taken -> 00010098
      7  00010018  050000ef  jal ra, fact              ra = 0x0001001c, -> 00010068
     42  00010064  00008067  jalr zero, 0(ra)          -> exit
      5  00010010  00000073  ecall                     ecall 5 (read int)
  ```
  The instruction column is the disassembly of the word (real instructions only: `li a7, 5` shows as
  `addi a7, zero, 5`), with branch and jump targets as labels where a label exists. Values print in
  signed decimal when |v| < 65536, else as `0x` and 8 hex digits. An ecall's line comes *before* what it
  prints; a changed `a0` (read int, sbrk) follows on a line of its own in the effect column. When the
  program's output leaves the cursor in mid-line, the next trace line starts on a new line. The trace ends
  with `exit status N after K steps`.
- `--stats` (after the run): instructions, loads, stores, branches (conditional, with how many were
  taken), jumps (`jal`, `jalr`), ecalls.
- `--regs` (after the run): `pc` and the 32 registers, four per line, by ABI name.
- `asm`: one line per word, `address  word  disassembly  source` (the source statement, labels kept, on
  the first word of each statement), then one line per data directive, `address  bytes  source` (at most 8
  bytes shown, then `...`). `--fields` adds a line per word with its fields in binary
  (`I  imm=111111110000 rs1=00010 f3=000 rd=00010 op=0010011`); `--hex` prints only the words, one per
  line, the input `dis` reads.
- `dis`: words in hex (whitespace-separated, `#` comments), disassembled from address `--base`
  (default `0x00010000`); a word outside the subset prints as `.word 0x…`.

## Python API

```python
from rv import assemble, Machine, run_source, decode, encode, disassemble, fields, AsmError, RVFault
```

- `assemble(text, name="<input>") -> Program` (raises `AsmError`, with `.line`, `.text`, `.msg`).
  `Program`: `.words` (list of int, at `.text_base` = 0x00010000 + 4i), `.lines[i]` = (line number, source
  line, first word of its statement?), `.data` (bytes at `.data_base` = 0x10000000), `.symbols`
  (label -> address), `.entry`, `.text_labels()` (address -> label), `.line_of(pc)`.
- `encode(mnemonic, rd=0, rs1=0, rs2=0, imm=0) -> int` (real instructions only; `imm` signed, a byte
  offset for branches and `jal`, the 20-bit field for `lui`/`auipc`; raises `EncodingError`).
  `decode(word) -> Instr | None` (`.mnemonic .fmt .rd .rs1 .rs2 .imm .word`).
  `disassemble(word, pc=None, symbols=None) -> str`; `fields(word) -> str`.
- `Machine(prog_or_text, inputs=None, stdin=None, out=None, echo=False)`:
  `inputs` is a list of numbers (or strings) read by ecall 5; without it, lines of `stdin` (default
  `sys.stdin`). Output is collected (`.output_text`) and also written to `out` if given.
  - State: `.x` (32 unsigned 32-bit ints; `.reg("a0")` reads one signed, `.set_reg(i, v)` writes),
    `.pc`, `.steps`, `.halted`, `.exit_code`, `.stats` (dict: instructions, loads, stores, branches,
    taken, jumps, ecalls), `.mem` (`.load/.store` through `.load(addr, size, signed=False)` and
    `.store(addr, size, value)` on the machine), `.read_string(addr)`, `.write(text)`, `.halt(code)`.
  - `.step() -> Step`, one instruction; `.run(max_steps=1_000_000, trace=None) -> exit status`, calling
    `trace(step)` after each instruction; raises `RVFault` (`.msg`, `.pc`: the faulting instruction),
    or its subclass `StepLimit`.
  - `.instruction_at(pc) -> (Instr | None, text) | None`: what is at an address, without running it.
- **The per-step record** `Step`: `pc`, `word`, `text` (disassembly), `kind` (`alu`, `muldiv`, `load`,
  `store`, `branch`, `jump`, `system`), `rd` and `rd_value` (the register written and its new unsigned
  value, or None; `x0` never appears), `srcs` (tuple of source registers read, `x0` left out),
  `mem_kind` (`load`/`store`/None), `mem_addr`, `mem_size` (1, 2, 4), `mem_value` (loaded after extension,
  or stored after truncation, unsigned), `branch_taken` (bool for conditional branches, else None),
  `next_pc`, `ecall` (the `a7` number, for an ecall), `trap` (see below). Book 4's pipeline, predictor and
  cache models are built on this record.
- **Hooks**, for chapters that extend the machine:
  - `.ecalls`: the system-call table, number -> `function(machine)`; add or replace entries.
  - `.on_ecall(machine, number) -> bool`: called for a number not in the table; return True if handled.
  - `.on_ebreak(machine)`: called for `ebreak`.
    These run inside the instruction; the machine then goes on to the next one (`pc + 4`).
  - `.on_trap(machine, cause)`: a **precise trap**. When it is set, every `ecall`, every `ebreak` and
    every word outside the subset (cause `"ecall"`, `"ebreak"`, `"illegal"`) calls it instead of the
    table and the two hooks above, with `.pc` still at that instruction; execution resumes at whatever
    `.pc` the handler leaves. A handler emulates the instruction and sets `m.pc += 4`; one that forgets
    runs the same instruction again, until the step limit. Each trap counts as one step and one
    instruction, and in `.traps`; its `Step` has `kind` `system` and `trap` = the cause. A handler may
    raise `RVFault` to stop the machine, or call `m.halt(code)`.
- `run_source(text, inputs=(), max_steps=1_000_000) -> (output, exit status, stats)`; raises on an
  assembly error or a fault.

## Determinism

No clock, no randomness, no addresses that depend on the host: the same program and input give the same
output, trace and counts on every machine. Output is flushed as it is written, so a fault's message
always follows what the program printed. About a million instructions take a second.

## Tests

`code/shared/rv/tests/` (`tools/test_code.sh shared` or `pytest code/shared/rv`): golden encodings
checked against the specification's layouts and the words GNU `as` prints; encode/decode and
disassemble/assemble round trips under hypothesis; the semantics of every edge case above (division,
shifts, extension, `li` at 0, ±1, 2047, 2048, −2048, −2049, 0x7ffff800, 0x80000000, 0xffffffff…); data
directives; every ecall; `sbrk`; every fault and assembly error message; the step record; the three
hooks; and the command line against golden transcripts (`tests/golden/`, programs in `tests/programs/`).
There is no external RISC-V simulator to compare with on this machine.

## Sources

The RISC-V Instruction Set Manual, Volume I: Unprivileged ISA (RV32I and M chapters, the tagged releases
of `riscv/riscv-isa-manual`); RISC-V International's `riscv-opcodes` tables (`extensions/rv_i`, `rv32_i`,
`rv_m`); the RISC-V ELF psABI (register names, stack alignment); the RISC-V Assembly Programmer's Manual
(pseudo-instructions, `call`/`tail`); the RARS system-call table; Linux's `asm-generic/unistd.h`.
Rows in `sources/ledger/book4.md`, accessed 2026-11-20.
