"""nested_walk.py -- the memory references of a two-stage address translation. The
guest's page tables (k levels) map a virtual address to a guest physical address; every
guest physical address, the guest's own table entries included, needs the host's walk
(h levels) before it can be read."""


def host_walk(h):  # guest physical -> host physical: one read per host level
    return [f"host L{level}" for level in range(h)]


def two_stage(k, h):
    refs = []
    for level in range(k):  # each guest entry lives at a guest physical address
        refs += host_walk(h) + [f"guest L{level}"]
    return refs + host_walk(h) + ["data"]  # and so does the data


if __name__ == "__main__":
    print("guest levels k  host levels h  references before the data  k*h + k + h")
    for k, h in ((1, 1), (2, 2), (2, 3), (3, 3), (4, 4), (5, 5)):
        before = len(two_stage(k, h)) - 1
        print(f"{k:>14}  {h:>13}  {before:>26}  {k * h + k + h:>11}")
    print("k = h = 2:", ", ".join(two_stage(2, 2)))
