"""ftl.py -- a flash translation layer: pages are written once and erased only by whole
blocks. Random overwrites of a fraction u of the flash; greedy cleaning; write
amplification."""
import random

BLOCKS, PAGES = 64, 64  # 64 erase blocks of 64 pages


def simulate(u, writes=60_000, seed=1):
    rng = random.Random(seed)
    logical = int(u * BLOCKS * PAGES)
    where = {}  # logical page -> (block, page)
    valid = [set() for _ in range(BLOCKS)]  # the logical pages each block holds
    free = list(range(1, BLOCKS))  # erased blocks; block 0 is being filled
    current, used = 0, 0
    flash_writes, victims = 0, []

    def program(lp):  # write a logical page at the next free page
        nonlocal current, used
        if used == PAGES:
            current, used = free.pop(0), 0
        if lp in where:
            valid[where[lp][0]].discard(lp)  # the old copy becomes garbage
        where[lp] = (current, used)
        valid[current].add(lp)
        used += 1

    start = logical + writes // 3  # measure the last two thirds: the steady state
    for k in range(logical + writes):
        lp = k if k < logical else rng.randrange(logical)  # fill, then overwrite
        if k == start:
            flash_writes, victims = 0, []
        while not free:  # clean: erase the block with the fewest valid pages
            victim = min((b for b in range(BLOCKS) if b != current),
                         key=lambda b: len(valid[b]))
            victims.append(len(valid[victim]) / PAGES)
            free.append(victim)
            for page in list(valid[victim]):  # copy its valid pages out first
                program(page)
                flash_writes += 1
        program(lp)
        flash_writes += 1
    return flash_writes / (logical + writes - start), sum(victims) / len(victims)


if __name__ == "__main__":
    print(f"{BLOCKS} blocks of {PAGES} pages; the last 40,000 of 60,000 overwrites")
    print("   u  amplification  victim valid  1/(1 - victim)  1/(1 - u)")
    for pct in range(50, 95, 5):
        wa, v = simulate(pct / 100)
        print(f"{pct / 100:.2f}  {wa:13.2f}  {v:12.2f}  {1 / (1 - v):14.2f}"
              f"  {1 / (1 - pct / 100):9.2f}")
