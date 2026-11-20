"""trace_demo.py: the loads of matrix_sum.S on rv, in a 1 KiB direct-mapped cache."""
from cache import Cache
from rv import Machine


def load_addresses(order):
    m = Machine(open("matrix_sum.S").read(), inputs=[order])
    loads = []
    m.run(trace=lambda s: loads.append(s.mem_addr) if s.mem_kind == "load" else None)
    return m.output_text, loads


def main():
    for order, name in [(0, "row order"), (1, "column order")]:
        out, loads = load_addresses(order)
        c = Cache(size=1024, line=32, ways=1)
        for addr in loads:
            c.access(addr)
        print(f"{name:<13} sum {out}  {len(loads)} loads  {c.hits:>4} hits"
              f"  {c.misses:>4} misses  miss ratio {c.miss_ratio():.3f}")
        print("  first addresses:", " ".join(f"{a:#x}" for a in loads[:4]))


if __name__ == "__main__":
    main()
