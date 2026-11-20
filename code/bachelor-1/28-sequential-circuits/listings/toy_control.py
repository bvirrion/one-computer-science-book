"""toy_control.py: the toy machine as a datapath (registers, ALU, memory) driven by a
control unit, a Moore machine whose states each order one or two register transfers.
Checked instruction by instruction against the shared simulator."""

from pathlib import Path

from toymachine import OPS, Machine, assemble

# The control unit: state -> the register transfers it orders (its Moore output).
CONTROL = {
    "FETCH0": ("IR0 <- M[PC]", "PC <- PC+1"),
    "FETCH1": ("IR1 <- M[PC]", "PC <- PC+1"),
    "DECODE": (),
    "LOADI": ("R <- IR1",), "LOAD": ("R <- M[IR1]",), "STORE": ("M[IR1] <- R",),
    "ALU_RR": ("R <- ALU(R, S)",), "ALU_RI": ("R <- ALU(R, IR1)",),
    "ALU_R": ("R <- ALU(R)",), "CMP": ("FLAGS <- ALU(R, S)",),
    "JUMP": ("PC <- IR1",), "IN": ("R <- IN",), "OUT": ("OUT <- R",),
    "LOADR": ("R <- M[S]",), "STORER": ("M[S] <- R",),
    "PUSH1": ("SP <- SP-1",), "PUSH2": ("M[SP] <- R",),
    "POP": ("R <- M[SP]", "SP <- SP+1"),
    "CALL1": ("SP <- SP-1",), "CALL2": ("M[SP] <- PC", "PC <- IR1"),
    "RET": ("PC <- M[SP]", "SP <- SP+1"),
    "HALT": ("PC <- PC-2",), "STOP": (),
}
GROUP = {"ADD": "ALU_RR", "SUB": "ALU_RR", "AND": "ALU_RR", "OR": "ALU_RR",
         "XOR": "ALU_RR", "ADDI": "ALU_RI", "NOT": "ALU_R", "SHL": "ALU_R",
         "SHR": "ALU_R", "JMP": "JUMP", "PUSH": "PUSH1", "CALL": "CALL1",
         "NOP": "FETCH0"}
TAKEN = {"JZ": ("Z", 1), "JNZ": ("Z", 0), "JN": ("N", 1), "JC": ("C", 1)}
AFTER = {"FETCH0": "FETCH1", "FETCH1": "DECODE", "PUSH1": "PUSH2", "CALL1": "CALL2",
         "HALT": "STOP", "STOP": "STOP"}


def next_state(state, op, flags):
    """The control unit's next state, from its state, the opcode and the flags."""
    if state != "DECODE":
        return AFTER.get(state, "FETCH0")
    if op in TAKEN:
        flag, value = TAKEN[op]
        return "JUMP" if flags[flag] == value else "FETCH0"
    return GROUP.get(op, op)


class Datapath:
    def __init__(self, mem, inputs):
        self.mem, self.inputs, self.outputs = list(mem), list(inputs), []
        self.reg, self.pc, self.sp, self.ir0, self.ir1 = [0] * 4, 0, 0, 0, 0
        self.flags = {"Z": 0, "N": 0, "C": 0}

    def alu(self, op, x, y=0):
        """The ALU of chapter 27, on eight bits: result and flags."""
        result, carry = {"ADD": (x + y, x + y > 255), "ADDI": (x + y, x + y > 255),
                         "SUB": (x - y, x < y), "CMP": (x - y, x < y),
                         "AND": (x & y, 0), "OR": (x | y, 0), "XOR": (x ^ y, 0),
                         "NOT": (~x, 0), "SHL": (x << 1, x >> 7),
                         "SHR": (x >> 1, x & 1)}[op]
        v = result % 256
        self.flags = {"Z": int(v == 0), "N": int(v >= 128), "C": int(carry)}
        return v

    def do(self, transfer):
        op, r, s = OPS[self.ir0 // 4][0], self.ir0 % 4, self.ir1 % 4
        R, M = self.reg, self.mem
        match transfer:
            case "IR0 <- M[PC]":
                self.ir0 = M[self.pc]
            case "IR1 <- M[PC]":
                self.ir1 = M[self.pc]
            case "PC <- PC+1":
                self.pc += 1
            case "PC <- PC-2":
                self.pc -= 2
            case "R <- IR1":
                R[r] = self.ir1
            case "R <- M[IR1]":
                R[r] = M[self.ir1]
            case "M[IR1] <- R":
                M[self.ir1] = R[r]
            case "R <- ALU(R, S)":
                R[r] = self.alu(op, R[r], R[s])
            case "R <- ALU(R, IR1)":
                R[r] = self.alu(op, R[r], self.ir1)
            case "R <- ALU(R)":
                R[r] = self.alu(op, R[r])
            case "FLAGS <- ALU(R, S)":
                self.alu(op, R[r], R[s])
            case "PC <- IR1":
                self.pc = self.ir1
            case "R <- IN":
                R[r] = self.inputs.pop(0) % 256
            case "OUT <- R":
                self.outputs.append(R[r])
            case "R <- M[S]":
                R[r] = M[R[s]]
            case "M[S] <- R":
                M[R[s]] = R[r]
            case "SP <- SP-1":
                self.sp = (self.sp - 1) % 256
            case "SP <- SP+1":
                self.sp = (self.sp + 1) % 256
            case "M[SP] <- R":
                M[self.sp] = R[r]
            case "R <- M[SP]":
                R[r] = M[self.sp]
            case "M[SP] <- PC":
                M[self.sp] = self.pc
            case "PC <- M[SP]":
                self.pc = M[self.sp]

    def snapshot(self):
        return (self.pc, self.sp, list(self.reg), dict(self.flags), list(self.mem),
                list(self.outputs))


def run(mem, inputs, trace=None, max_cycles=100_000):
    """Clock the control unit and the datapath; compare with the shared simulator after
    every instruction. Returns (instructions, cycles)."""
    d, ref, state = Datapath(mem, inputs), Machine(mem, inputs), "FETCH0"
    instructions = cycles = 0
    while state != "STOP" and cycles < max_cycles:
        for transfer in CONTROL[state]:
            d.do(transfer)
        if trace:
            trace(cycles, state, d)
        cycles += 1
        state = next_state(state, OPS[d.ir0 // 4][0], d.flags)
        if state in ("FETCH0", "STOP"):  # an instruction is over
            instructions += 1
            ref.step()
            assert d.snapshot() == (ref.pc, ref.sp, ref.reg, ref.flags, ref.mem,
                                    ref.outputs)
    return instructions, cycles


def example_programs():
    """The toy programs of the earlier books, copied here with their inputs."""
    folder = Path(__file__).resolve().parents[1] / "programs"
    for path in sorted(folder.glob("*.toy")):
        stdin = path.with_suffix(".stdin")
        inputs = [int(x) for x in stdin.read_text().split()] if stdin.exists() else []
        yield path.stem, assemble(path.read_text()), inputs


if __name__ == "__main__":
    total_i = total_c = 0
    for name, mem, inputs in example_programs():
        i, c = run(mem, inputs)
        total_i, total_c = total_i + i, total_c + c
        print(f"{name:15} {i:3} instructions {c:4} cycles, "
              "as the simulator after each one")
    print(f"in all: {total_i} instructions, {total_c} cycles, "
          f"{total_c / total_i:.2f} cycles per instruction")
