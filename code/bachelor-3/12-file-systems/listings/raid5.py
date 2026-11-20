"""raid5.py -- data striped over five disks with a rotating parity block; one disk is
lost, and rebuilt from the four others by XOR."""
import hashlib
import random

DISKS, BLOCK = 5, 512


def xor(blocks):
    out = bytearray(BLOCK)
    for b in blocks:
        for i, byte in enumerate(b):
            out[i] ^= byte
    return bytes(out)


def stripe(data):  # -> disks[d] = list of blocks; the parity moves left each stripe
    disks = [[] for _ in range(DISKS)]
    blocks = [data[i:i + BLOCK] for i in range(0, len(data), BLOCK)]
    for s in range(len(blocks) // (DISKS - 1)):
        group = blocks[s * (DISKS - 1):(s + 1) * (DISKS - 1)]
        p = DISKS - 1 - s % DISKS  # the parity's disk in stripe s
        row = group[:p] + [xor(group)] + group[p:]
        for d in range(DISKS):
            disks[d].append(row[d])
    return disks


def read_back(disks):
    out = b""
    for s in range(len(disks[0])):
        p = DISKS - 1 - s % DISKS
        out += b"".join(disks[d][s] for d in range(DISKS) if d != p)
    return out


if __name__ == "__main__":
    rng = random.Random(5)
    data = bytes(rng.randrange(256) for _ in range(40 * BLOCK))  # 20 KiB: 10 stripes
    disks = stripe(data)
    print("disk:    " + " ".join(f"{d:>4}" for d in range(DISKS)))
    for s in range(5):
        p = DISKS - 1 - s % DISKS
        names, k = [], s * (DISKS - 1)
        for d in range(DISKS):
            names.append("P" if d == p else f"D{k}")
            k += d != p
        print(f"stripe {s}: " + " ".join(f"{n:>4}" for n in names))
    print("data   ", hashlib.sha256(data).hexdigest()[:16])
    lost = disks[2]
    disks[2] = None  # disk 2 fails
    disks[2] = [xor([disks[d][s] for d in range(DISKS) if d != 2])
                for s in range(len(lost))]
    print("rebuilt", hashlib.sha256(read_back(disks)).hexdigest()[:16],
          "disk 2 identical:", disks[2] == lost)
