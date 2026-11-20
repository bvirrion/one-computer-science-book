"""Write joins.dat: measured page I/O of four joins as R grows from 100 to 1,000
pages, S fixed at 100 pages (a key), 12 buffer pages. The tuple nested loop is left
out: at 100 pages it already costs 100,100."""

import random
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "listings"))
from exec import Disk, Relation  # noqa: E402
from joins import (  # noqa: E402
    block_nested_loop,
    build_index,
    hash_join,
    index_nested_loop,
    sort_merge,
)


def main() -> None:
    rng = random.Random(22)
    S = Relation({"book_id": j} for j in range(1000))
    tree = build_index(S, "book_id")
    lines = ["M bnl inl sm hash\n"]
    for M in range(100, 1001, 100):
        R = Relation({"book": rng.randrange(1000)} for _ in range(10 * M))
        row = [M]
        for run in (
            lambda d, R=R: block_nested_loop(R, S, "book", "book_id", 12, d),
            lambda d, R=R: index_nested_loop(R, S, "book", "book_id", tree, d),
            lambda d, R=R: sort_merge(R, S, "book", "book_id", 12, d),
            lambda d, R=R: hash_join(R, S, "book", "book_id", 12, d),
        ):
            disk = Disk()
            run(disk)
            row.append(disk.io())
        lines.append(" ".join(map(str, row)) + "\n")
    (HERE / "joins.dat").write_text("".join(lines))


if __name__ == "__main__":
    main()
