"""table_size.py -- how much memory Sv32 page tables take for a few layouts of an
address space, against a one-level table with an entry for each of the 2**20 pages."""

PAGE, MB = 4096, 1 << 20


def pages(regions):  # regions: (start address, length in bytes)
    return {va // PAGE for start, n in regions for va in range(start, start + n, PAGE)}


def table_bytes(regions):
    used = pages(regions)
    level0 = {vpn >> 10 for vpn in used}  # one level-0 table per 4 MiB touched
    return len(used), len(level0), (1 + len(level0)) * PAGE


LAYOUTS = {
    "small program": [(0x00010000, 200 * 1024), (0x10000000, 2 * MB),
                      (0x40000000, MB), (0x80000000 - 128 * 1024, 128 * 1024)],
    "1 GiB array": [(0x10000000, 1024 * MB)],
    "64 scattered pages": [(k * 4 * MB, PAGE) for k in range(64)],
}
ONE_LEVEL = 2**20 * 4  # 2**20 entries of 4 bytes

print(f"{'layout':<20}{'pages':>8}{'tables':>8}{'table bytes':>13}{'per page':>10}")
for name, regions in LAYOUTS.items():
    n, t, size = table_bytes(regions)
    print(f"{name:<20}{n:>8}{t + 1:>8}{size:>13,}{size / n:>10.1f}")
print(f"one-level table: {ONE_LEVEL:,} bytes, whatever the layout")
