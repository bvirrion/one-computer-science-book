"""ex5_redo.py -- a recovery whose redo pass reapplies only the records of committed
transactions, "since the others will be undone anyway". It is run at every crash
point of crash_all's workload, then the fix: repeat all of history."""

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from crash_all import expected, workload  # noqa: E402
from minidb import analysis, page_of, redo, undo  # noqa: E402


def redo_committed(log, pages, dpt, say):
    """The bug: records of transactions without a commit record are skipped."""
    committed = {r["txn"] for r in log if r["kind"] == "commit"}
    for r in log:
        if r["kind"] in ("update", "clr") and r["txn"] in committed:
            p = pages[page_of(r["item"])]
            if p["lsn"] < r["lsn"]:
                p["items"][r["item"]], p["lsn"] = r["after"], r["lsn"]


def recover_with(redo_pass, log, pages):
    log, pages = copy.deepcopy(log), copy.deepcopy(pages)
    losers, dpt = analysis(log)
    redo_pass(log, pages, dpt, lambda s: None)
    undo(log, pages, losers, lambda s: None)
    return {k: v for p in pages.values() for k, v in p["items"].items()}


def failures(redo_pass):
    out = []
    for i, (kind, what, (log, pages)) in enumerate(workload().events):
        got = recover_with(redo_pass, log, pages)
        if got != expected(log):
            wrong = {k: v for k, v in got.items() if v != expected(log)[k]}
            out.append((i + 1, kind, what, wrong))
    return out


if __name__ == "__main__":
    for name, redo_pass in (
        ("committed only", redo_committed),
        ("repeat history", redo),
    ):
        bad = failures(redo_pass)
        print(f"{name}: {len(bad)} wrong recoveries")
        for crash, kind, what, wrong in bad:
            print(f"  crash {crash} (after {kind} {what}): wrong values {wrong}")
