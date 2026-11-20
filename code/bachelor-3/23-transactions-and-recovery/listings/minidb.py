"""minidb.py -- a tiny database of named items on pages, with a write-ahead log and
recovery in the style of ARIES. The buffer pool may write a page holding uncommitted
changes (steal) and need not write any page at commit (no force); the WAL rule
holds: a page reaches the disk only after the log records of its changes. Every
durable event (a log record flushed, a page written) is recorded, so that a crash
can be simulated after any of them."""

import copy


def page_of(item):
    return (ord(item) - ord("a")) // 2  # two items per page: a b | c d | e f | g h


class Disk:
    def __init__(self, items):
        self.log = []  # the durable log
        self.pages = {}
        for item, value in items.items():
            self.pages.setdefault(page_of(item), {"lsn": 0, "items": {}})["items"][
                item
            ] = value


class MiniDB:
    def __init__(self, items):
        self.disk = Disk(items)
        self.buffer = copy.deepcopy(self.disk.pages)
        self.tail, self.last, self.dirty = [], {}, {}  # unflushed log, txn -> last LSN
        self.lsn, self.events = 0, []

    def append(self, **rec):
        self.lsn += 1
        rec["lsn"] = self.lsn
        self.tail.append(rec)
        return rec

    def flush_log(self, upto):
        while self.tail and self.tail[0]["lsn"] <= upto:
            self.disk.log.append(self.tail.pop(0))
            self.events.append(("log", self.disk.log[-1]["lsn"], self.snapshot()))

    def snapshot(self):
        return copy.deepcopy((self.disk.log, self.disk.pages))

    def update(self, t, item, value):
        p = self.buffer[page_of(item)]
        rec = self.append(
            kind="update",
            txn=t,
            item=item,
            before=p["items"][item],
            after=value,
            prev=self.last.get(t),
        )
        self.last[t] = rec["lsn"]
        p["items"][item], p["lsn"] = value, rec["lsn"]
        self.dirty.setdefault(page_of(item), rec["lsn"])  # recLSN: first change

    def write_page(self, pid):
        self.flush_log(self.buffer[pid]["lsn"])  # the WAL rule
        self.disk.pages[pid] = copy.deepcopy(self.buffer[pid])
        self.dirty.pop(pid, None)
        self.events.append(("page", pid, self.snapshot()))

    def commit(self, t):
        rec = self.append(kind="commit", txn=t, prev=self.last[t])
        self.flush_log(rec["lsn"])  # a commit is durable once its record is
        self.append(kind="end", txn=t, prev=rec["lsn"])
        del self.last[t]

    def rollback(self, t):
        """Undo t's updates newest first, logging each undo as a CLR."""
        lsn = self.last[t]
        while lsn is not None:
            rec = next(r for r in self.disk.log + self.tail if r["lsn"] == lsn)
            p = self.buffer[page_of(rec["item"])]
            clr = self.append(
                kind="clr",
                txn=t,
                item=rec["item"],
                after=rec["before"],
                undo_next=rec["prev"],
                prev=self.last[t],
            )
            self.last[t] = clr["lsn"]
            p["items"][rec["item"]], p["lsn"] = rec["before"], clr["lsn"]
            self.dirty.setdefault(page_of(rec["item"]), clr["lsn"])
            lsn = rec["prev"]
        self.append(kind="end", txn=t, prev=self.last.pop(t))

    def checkpoint(self):
        rec = self.append(kind="checkpoint", att=dict(self.last), dpt=dict(self.dirty))
        self.flush_log(rec["lsn"])


def analysis(log):
    """From the last checkpoint on: the losers with their last LSN, and the dirty
    page table, each page with the LSN of the first change that may not be on disk."""
    start = max((i for i, r in enumerate(log) if r["kind"] == "checkpoint"), default=-1)
    att = dict(log[start]["att"]) if start >= 0 else {}
    dpt = dict(log[start]["dpt"]) if start >= 0 else {}
    for r in log[start + 1 :]:
        if r["kind"] in ("update", "clr"):
            att[r["txn"]] = r["lsn"]
            dpt.setdefault(page_of(r["item"]), r["lsn"])
        elif r["kind"] == "commit":
            att[r["txn"]] = "committed"
        elif r["kind"] == "end":
            att.pop(r["txn"], None)
    return {t: lsn for t, lsn in att.items() if lsn != "committed"}, dpt


def redo(log, pages, dpt, say):
    """Repeat history: reapply every update and CLR not yet on its page."""
    first, skipped = min(dpt.values(), default=None), 0
    for r in log:
        if first is None or r["lsn"] < first or r["kind"] not in ("update", "clr"):
            continue
        p = pages[page_of(r["item"])]
        if (
            r["lsn"] >= dpt.get(page_of(r["item"]), float("inf"))
            and p["lsn"] < r["lsn"]
        ):
            p["items"][r["item"]], p["lsn"] = r["after"], r["lsn"]
            say(f"redo {r['lsn']}: {r['item']} = {r['after']}")
        else:
            skipped += 1
    say(f"redo from LSN {first}: {skipped} records skipped, already on disk")


def undo(log, pages, losers, say, crash_after=None):
    """Roll the losers back, newest record first, logging a CLR for each update
    undone; a CLR met on the way sends the walk to its undo_next."""
    lsn, by_lsn = max((r["lsn"] for r in log), default=0), {r["lsn"]: r for r in log}
    todo, written = dict(losers), 0
    while todo:
        t = max(todo, key=todo.get)
        r = by_lsn[todo[t]]
        nxt = r["undo_next"] if r["kind"] == "clr" else r["prev"]
        if r["kind"] == "update":
            if written == crash_after:
                return False  # the crash: the CLRs logged so far are durable
            lsn += 1
            log.append(
                {
                    "lsn": lsn,
                    "kind": "clr",
                    "txn": t,
                    "item": r["item"],
                    "after": r["before"],
                    "undo_next": nxt,
                    "prev": todo[t],
                }
            )
            written += 1
            p = pages[page_of(r["item"])]
            p["items"][r["item"]], p["lsn"] = r["before"], lsn
            say(f"undo {r['lsn']}: {r['item']} = {r['before']} (CLR {lsn})")
        if nxt is None:
            lsn += 1
            log.append({"lsn": lsn, "kind": "end", "txn": t, "prev": todo.pop(t)})
        else:
            todo[t] = nxt
    return True


def recover(log, pages, trace=None, crash_after=None):
    """Analysis, redo and undo on copies of a durable log and pages; returns the item
    values (None after a crash during recovery) and the log as recovery extended it.
    trace, a list, receives what each pass does; crash_after=k crashes recovery
    before its (k+1)-th CLR."""
    log, pages = copy.deepcopy(log), copy.deepcopy(pages)
    say = trace.append if trace is not None else (lambda s: None)
    losers, dpt = analysis(log)
    say(f"analysis: losers {sorted(losers)}, dirty pages {dict(sorted(dpt.items()))}")
    redo(log, pages, dpt, say)
    if not undo(log, pages, losers, say, crash_after):
        return None, log
    return {k: v for p in pages.values() for k, v in p["items"].items()}, log
