import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def run(tmp_path, text):
    f = tmp_path / "q.sql"
    f.write_text(text)
    return subprocess.run([sys.executable, str(HERE / "sqlrun.py"), str(f)], capture_output=True,
                          text=True, check=True).stdout


def test_create_insert_select(tmp_path):
    out = run(tmp_path, "CREATE TABLE t (a INTEGER, b TEXT);\nINSERT INTO t VALUES (1, 'x'), (22, NULL);\n"
                        "SELECT a, b\n  FROM t ORDER BY a;\n")
    assert out.splitlines() == [
        "sql> CREATE TABLE t (a INTEGER, b TEXT);", "OK", "",
        "sql> INSERT INTO t VALUES (1, 'x'), (22, NULL);", "OK (2 rows changed)", "",
        "sql> SELECT a, b", "...>   FROM t ORDER BY a;",
        "+----+------+", "| a  | b    |", "+----+------+", "| 1  | x    |", "| 22 | NULL |",
        "+----+------+", "(2 rows)", ""]


def test_error_goes_on_and_load_directive(tmp_path):
    (tmp_path / "schema.sql").write_text("CREATE TABLE u (n INTEGER PRIMARY KEY);\nINSERT INTO u VALUES (7);\n")
    out = run(tmp_path, "-- load: schema.sql\nSELECT * FROM nope;\nSELECT n FROM u;\n")
    assert "Error: no such table: nope" in out and "| 7 |" in out and "CREATE" not in out


def test_town_directive(tmp_path):
    out = run(tmp_path, "-- load: town\nSELECT COUNT(*) AS n FROM places;\n")
    assert "| 30 |" in out
