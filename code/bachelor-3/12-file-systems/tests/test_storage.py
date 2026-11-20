"""Tests for the disk schedulers, the flash translation layer, RAID 5 and the file-size
arithmetic, with exercises 2, 9 and 11."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))

import ftl  # noqa: E402
import max_file  # noqa: E402
import raid5  # noqa: E402
from disk_sched import fcfs, scan, sstf, travel  # noqa: E402


def test_exercise_2_scan_by_hand():
    queue = [82, 17, 43, 140, 24, 16, 190]
    assert scan(50, queue) == [82, 140, 190, 43, 24, 17, 16]
    assert travel(50, scan(50, queue), scan) == 332


def test_every_request_is_served_and_scan_is_bounded():
    rng = random.Random(7)
    for _ in range(200):
        queue = [rng.randrange(200) for _ in range(rng.randint(1, 15))]
        head = rng.randrange(200)
        assert sorted(sstf(head, queue)) == sorted(queue) == sorted(scan(head, queue))
        assert travel(head, scan(head, queue), scan) <= 2 * 199
        assert len(fcfs(head, queue)) == len(queue)


def test_exercise_11_sstf_starves():
    # a request at 190 waits while requests keep arriving near the head at 50
    head, waiting, served = 50, [190], 0
    for k in range(100):
        waiting.append(50 + (k % 3))
        nxt = sstf(head, waiting)[0]
        waiting.remove(nxt)
        head = nxt
        served += nxt == 190
    assert served == 0 and 190 in waiting


def test_write_amplification_matches_the_victims():
    wa, v = ftl.simulate(0.8)
    assert abs(wa - 1 / (1 - v)) < 0.01 and wa < 1 / (1 - 0.8)


def test_exercise_9_parity_by_hand():
    a, b, c, d = 0x3C, 0xA5, 0x0F, 0x81
    p = a ^ b ^ c ^ d
    assert p == 0x17 and a ^ c ^ d ^ p == b


def test_raid5_rebuilds_any_disk():
    data = bytes(random.Random(9).randrange(256) for _ in range(8 * 4 * raid5.BLOCK))
    for lost in range(raid5.DISKS):
        disks = raid5.stripe(data)
        gone = disks[lost]
        disks[lost] = [raid5.xor([disks[d][s] for d in range(raid5.DISKS) if d != lost])
                       for s in range(len(gone))]
        assert disks[lost] == gone and raid5.read_back(disks) == data


def test_largest_files():
    def total(block):
        return sum(n for _, n, _ in max_file.regions(block)) * block

    assert total(4096) == (12 + 1024 + 1024**2 + 1024**3) * 4096 == 4_402_345_721_856
    assert total(1024) // 2**30 == 16 and total(2048) // 2**30 == 256
