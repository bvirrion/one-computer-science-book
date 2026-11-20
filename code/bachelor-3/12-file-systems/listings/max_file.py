"""max_file.py -- the largest file an inode with 12 direct pointers and one single, one
double and one triple indirect pointer can describe, and the reads to reach each
part."""


def regions(block, pointer=4, direct=12):
    n = block // pointer  # block numbers per pointer block
    sizes = [direct, n, n**2, n**3]  # blocks reached through each kind of pointer
    names = ["direct", "single indirect", "double indirect", "triple indirect"]
    return list(zip(names, sizes, [2, 3, 4, 5]))  # reads: inode, pointer blocks, data


def human(nbytes):
    for unit in ("bytes", "KiB", "MiB", "GiB", "TiB"):
        if nbytes < 1024:
            return f"{nbytes:.1f} {unit}" if unit != "bytes" else f"{nbytes} bytes"
        nbytes /= 1024
    return f"{nbytes:.1f} PiB"


for block in (1024, 2048, 4096):
    print(f"blocks of {block} bytes, 4-byte block numbers:")
    total = 0
    for name, blocks, reads in regions(block):
        total += blocks * block
        print(f"  {name:<16} {blocks:>13,} blocks  {human(blocks * block):>10}"
              f"  {reads} reads")
    print(f"  largest file: {total:,} bytes = {human(total)}")
