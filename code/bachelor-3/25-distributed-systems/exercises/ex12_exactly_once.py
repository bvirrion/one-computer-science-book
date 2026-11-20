"""Exercise 12: a deposit server that survives crashes. Balances and the log of replies
live in an SQLite file. The server can crash at three points of a request; the client
retries the same request id until it gets a reply. `atomic` says whether executing and
logging the reply are one transaction or two."""

import sqlite3

POINTS = ("before executing", "after executing", "after logging")


class Server:
    def __init__(self, path, atomic):
        self.path, self.atomic, self.crash_at = path, atomic, None
        with sqlite3.connect(path) as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS account (name TEXT PRIMARY KEY, bal INT)"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS reply (id TEXT PRIMARY KEY, result INT)"
            )
            db.execute("CREATE TABLE IF NOT EXISTS runs (n INT)")
            db.execute("INSERT OR IGNORE INTO account VALUES ('bakery', 0)")

    def deposit(self, rid, amount):
        """Returns the new balance, or raises ConnectionError where it crashes."""
        db = sqlite3.connect(self.path, isolation_level=None)
        try:
            old = db.execute("SELECT result FROM reply WHERE id = ?", (rid,)).fetchone()
            if old:
                return old[0]  # a duplicate: answered from the log
            self.crash("before executing")
            db.execute("BEGIN")
            db.execute(
                "UPDATE account SET bal = bal + ? WHERE name = 'bakery'", (amount,)
            )
            db.execute("INSERT INTO runs VALUES (1)")
            bal = db.execute("SELECT bal FROM account").fetchone()[0]
            if not self.atomic:
                db.execute("COMMIT")
            self.crash("after executing")  # with atomic: inside the open transaction
            if not self.atomic:
                db.execute("BEGIN")
            db.execute("INSERT INTO reply VALUES (?, ?)", (rid, bal))
            db.execute("COMMIT")  # with atomic: the deposit and its reply together
            self.crash("after logging")
            return bal
        finally:
            db.close()  # a crash inside a transaction rolls it back

    def crash(self, point):
        if self.crash_at == point:
            self.crash_at = None  # the server restarts; the file survives
            raise ConnectionError(f"server crashed {point}")

    def executions(self):
        with sqlite3.connect(self.path) as db:
            return db.execute("SELECT count(*) FROM runs").fetchone()[0]


def client(server, rid, amount, tries=5):
    for _ in range(tries):
        try:
            return server.deposit(rid, amount)
        except ConnectionError:
            continue
    raise TimeoutError(rid)


def trial(path, atomic, point):
    srv = Server(path, atomic)
    srv.crash_at = point
    client(srv, "c-1", 10)
    return srv.executions()


if __name__ == "__main__":
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as d:
        for atomic in (False, True):
            for i, point in enumerate(POINTS):
                n = trial(str(Path(d) / f"{atomic}{i}.db"), atomic, point)
                print(f"atomic={atomic!s:<5} crash {point:<16}: executed {n} time(s)")
