"""Milestone 2: a two-pass assembler for the toy machine."""
from tokens import is_name, parse_number, read_program

OPS = [("HALT", ""), ("LOADI", "rn"), ("LOAD", "r[a]"), ("STORE", "r[a]"),
       ("ADD", "rs"), ("SUB", "rs"), ("ADDI", "rn"), ("AND", "rs"), ("OR", "rs"),
       ("XOR", "rs"), ("NOT", "r"), ("SHL", "r"), ("SHR", "r"), ("CMP", "rs"),
       ("JMP", "a"), ("JZ", "a"), ("JNZ", "a"), ("JN", "a"), ("JC", "a"),
       ("IN", "r"), ("OUT", "r"), ("LOADR", "rs"), ("STORER", "rs"), ("PUSH", "r"),
       ("POP", "r"), ("CALL", "a"), ("RET", ""), ("NOP", "")]
OPCODE = {name: i for i, (name, _) in enumerate(OPS)}
KIND = dict(OPS)
OPERANDS = {"": 0, "r": 1, "a": 1, "rn": 2, "rs": 2, "r[a]": 2}
REGISTERS = ["R0", "R1", "R2", "R3"]


def size(mnemonic, operands, line):
    """How many bytes a line places in memory."""
    if mnemonic == "DATA":
        if not operands:
            raise ValueError(f"line {line}: DATA needs at least one number")
        return len(operands)
    if mnemonic not in OPCODE:
        raise ValueError(f"line {line}: unknown instruction {mnemonic!r}")
    return 2


def first_pass(rows):
    """The symbol table: each label, and the address of what follows it."""
    symbols, address = {}, 0
    for line, label, mnemonic, operands in rows:
        if label:
            if label in symbols:
                raise ValueError(f"line {line}: label {label!r} is defined twice")
            symbols[label] = address
        if mnemonic:
            address += size(mnemonic, operands, line)
    if address > 256:
        raise ValueError(f"the program needs {address} bytes; the memory has 256")
    return symbols


def register(tok, line):
    if tok.upper() not in REGISTERS:
        raise ValueError(f"line {line}: {tok!r} is not a register (R0 to R3)")
    return int(tok[1])


def value(tok, symbols, line):
    """A number, or a label replaced by its address from the symbol table."""
    if is_name(tok) and tok.upper() not in REGISTERS:
        if tok not in symbols:
            raise ValueError(f"line {line}: label {tok!r} is used but not defined")
        return symbols[tok]
    return parse_number(tok, line)


def encode(mnemonic, operands, symbols, line):
    """The bytes of one line: [4 * opcode + r, operand], or the bytes of DATA."""
    if mnemonic == "DATA":
        return [value(op, symbols, line) for op in operands]
    kind = KIND[mnemonic]
    if len(operands) != OPERANDS[kind]:
        raise ValueError(f"line {line}: {mnemonic} takes {OPERANDS[kind]} operand(s),"
                         f" got {len(operands)}")
    r = register(operands[0], line) if kind.startswith("r") else 0
    operand = 0
    if kind == "rn":
        operand = value(operands[1], symbols, line)
    elif kind == "rs":
        operand = register(operands[1], line)
    elif kind == "r[a]":
        inside = operands[1]
        if not (inside.startswith("[") and inside.endswith("]")):
            raise ValueError(f"line {line}: {mnemonic} wants an address in brackets")
        operand = value(inside[1:-1].strip(), symbols, line)
    elif kind == "a":
        operand = value(operands[0], symbols, line)
    return [4 * OPCODE[mnemonic] + r, operand]


def second_pass(rows, symbols):
    """[(address, bytes, line number)] for every line that places bytes."""
    placed, address = [], 0
    for line, _label, mnemonic, operands in rows:
        if mnemonic:
            data = encode(mnemonic, operands, symbols, line)
            placed.append((address, data, line))
            address += len(data)
    return placed


def assemble(text):
    """The 256 bytes of memory holding the program, from address 0."""
    rows = read_program(text)
    memory = [0] * 256
    for address, data, _line in second_pass(rows, first_pass(rows)):
        memory[address:address + len(data)] = data
    return memory
