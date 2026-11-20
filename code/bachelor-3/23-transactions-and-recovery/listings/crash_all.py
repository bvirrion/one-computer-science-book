"""crash_all.py -- one workload of five transactions on minidb, a crash simulated
after every durable event, recovery run on what the disk holds, and the result
checked: every committed transaction's writes present, no other transaction's."""

from minidb import MiniDB, recover

INITIAL = {k: 0 for k in "abcdefgh"}


def workload():
    db = MiniDB(INITIAL)
    db.update(1, "a", 10)
    db.update(2, "c", 20)
    db.update(1, "b", 11)
    db.write_page(1)  # steal: T2's uncommitted c goes to disk
    db.commit(1)
    db.update(3, "e", 30)
    db.write_page(2)  # steal again: T3's e goes to disk, then T3 aborts
    db.update(2, "d", 21)
    db.checkpoint()
    db.update(4, "g", 40)
    db.update(3, "f", 31)
    db.rollback(3)  # T3 aborts: its two updates are undone, with CLRs
    db.write_page(2)
    db.commit(2)
    db.update(5, "h", 50)
    db.update(4, "a", 41)
    db.write_page(0)
    db.write_page(3)  # T4 and T5 never commit
    db.update(5, "e", 51)
    db.flush_log(db.lsn)
    return db


def expected(log):
    """The writes of the transactions whose commit record is durable, in log order."""
    done = {r["txn"] for r in log if r["kind"] == "commit"}
    values = dict(INITIAL)
    for r in log:
        if r["kind"] == "update" and r["txn"] in done:
            values[r["item"]] = r["after"]
    return values


def disk_values(pages):
    return {k: v for p in pages.values() for k, v in p["items"].items()}


if __name__ == "__main__":
    db = workload()
    good = raw = again = tries = 0
    for i, (kind, what, (log, pages)) in enumerate(db.events):
        values, full = recover(log, pages)
        ok = values == expected(log)
        good += ok
        raw += disk_values(pages) == expected(log)
        clrs = sum(r["kind"] == "clr" for r in full) - sum(
            r["kind"] == "clr" for r in log
        )
        for k in range(clrs):  # crash again after k CLRs of the recovery
            _, partial = recover(log, pages, crash_after=k)
            again += recover(partial, pages)[0] == expected(log)
            tries += 1
        event = (
            f"log record {what} flushed" if kind == "log" else f"page {what} written"
        )
        done = sorted(r["txn"] for r in log if r["kind"] == "commit")
        print(f"crash {i + 1:>2}, after {event:<21} committed {str(done):<7} ok: {ok}")
    print(
        f"{good} of {len(db.events)} crashes recover consistently; "
        f"{raw} disks were consistent before recovery"
    )
    print(f"{again} of {tries} crashes during undo recover consistently")
