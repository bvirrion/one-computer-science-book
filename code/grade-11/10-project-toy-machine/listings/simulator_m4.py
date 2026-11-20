"""Milestone 4: flags, jumps, input, the stack and subroutines: all 28 instructions."""
import simulator_m3

new_machine = simulator_m3.new_machine          # offered again by this module
step = simulator_m3.step


def set_flags(m, result, carry=0):
    """Keep the result modulo 256 and set Z, N and C from it."""
    v = result % 256
    m["flags"] = {"Z": int(v == 0), "N": int(v >= 128), "C": int(carry)}
    return v


def add(m, r, s):
    total = m["reg"][r] + m["reg"][s % 4]
    m["reg"][r] = set_flags(m, total, total > 255)


def addi(m, r, n):
    total = m["reg"][r] + n
    m["reg"][r] = set_flags(m, total, total > 255)


def sub(m, r, s):
    a, b = m["reg"][r], m["reg"][s % 4]
    m["reg"][r] = set_flags(m, a - b, a < b)        # C: a borrow was needed


def cmp(m, r, s):
    a, b = m["reg"][r], m["reg"][s % 4]
    set_flags(m, a - b, a < b)                       # the flags only


def jump_if(m, flag, wanted, a):
    if m["flags"][flag] == wanted:
        m["pc"] = a


def jz(m, r, a):
    jump_if(m, "Z", 1, a)


def jnz(m, r, a):
    jump_if(m, "Z", 0, a)


def jn(m, r, a):
    jump_if(m, "N", 1, a)


def jc(m, r, a):
    jump_if(m, "C", 1, a)


def read(m, r, b):
    if not m["inputs"]:
        raise RuntimeError("IN: no input left")
    v = m["inputs"].pop(0)
    if not -128 <= v <= 255:
        raise RuntimeError(f"IN: {v} does not fit in one byte")
    m["reg"][r] = v % 256


def loadr(m, r, s):
    m["reg"][r] = m["mem"][m["reg"][s % 4]]


def storer(m, r, s):
    m["mem"][m["reg"][s % 4]] = m["reg"][r]


def push_value(m, v):
    m["sp"] = (m["sp"] - 1) % 256                    # the stack grows downward
    m["mem"][m["sp"]] = v


def pop_value(m):
    v = m["mem"][m["sp"]]
    m["sp"] = (m["sp"] + 1) % 256
    return v


def push(m, r, b):
    push_value(m, m["reg"][r])


def pop(m, r, b):
    m["reg"][r] = pop_value(m)


def call(m, r, a):
    push_value(m, m["pc"])                     # PC already holds the next address
    m["pc"] = a


def ret(m, r, b):
    m["pc"] = pop_value(m)


def logic(operation):
    def execute(m, r, s):
        m["reg"][r] = set_flags(m, operation(m["reg"][r], m["reg"][s % 4]))
    return execute


def not_(m, r, b):
    m["reg"][r] = set_flags(m, ~m["reg"][r] & 255)


def shl(m, r, b):
    m["reg"][r] = set_flags(m, m["reg"][r] << 1, m["reg"][r] >> 7)


def shr(m, r, b):
    m["reg"][r] = set_flags(m, m["reg"][r] >> 1, m["reg"][r] & 1)


EXECUTE = simulator_m3.EXECUTE | {
    4: add, 5: sub, 6: addi, 7: logic(lambda a, b: a & b),
    8: logic(lambda a, b: a | b), 9: logic(lambda a, b: a ^ b), 10: not_, 11: shl,
    12: shr, 13: cmp, 15: jz, 16: jnz, 17: jn, 18: jc, 19: read, 21: loadr,
    22: storer, 23: push, 24: pop, 25: call, 26: ret}


def run(m, max_steps=10_000, trace=None):
    """Step until HALT with all 28 instructions."""
    return simulator_m3.run(m, max_steps, EXECUTE, trace)
