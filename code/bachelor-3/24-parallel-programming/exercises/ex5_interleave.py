"""ex5_interleave.py -- what `total += a[i]` does when two threads run it on one shared
total: each += is a load into a register, an add, a store. A scripted interleaving
of the two threads shows the update that is lost."""


def run(a_parts, script):
    """a_parts: the numbers each thread adds; script: which thread takes each step."""
    total, regs, pos, phase = 0, [0, 0], [0, 0], [0, 0]
    for t in script:
        if pos[t] == len(a_parts[t]):
            continue
        if phase[t] == 0:
            regs[t] = total  # load
        elif phase[t] == 1:
            regs[t] += a_parts[t][pos[t]]  # add
        else:
            total = regs[t]  # store
            pos[t] += 1
        print(f"thread {t} {('load', 'add', 'store')[phase[t]]:<5} total={total}")
        phase[t] = (phase[t] + 1) % 3
    return total


if __name__ == "__main__":
    parts = ([5, 7], [3, 4])
    print(
        "final total:",
        run(parts, [0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1]),
        "instead of",
        19,
    )
