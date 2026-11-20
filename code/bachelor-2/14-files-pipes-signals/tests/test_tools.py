"""mycp, tee and minish2 on generated files; the copy law counted with strace."""
import os
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent.parent
E, L = HERE / "exercises", HERE / "listings"


@pytest.fixture(scope="module")
def bins(tmp_path_factory):
    d = tmp_path_factory.mktemp("bin")
    for name, src in [("mycp", E / "mycp.c"), ("tee", E / "tee.c"), ("minish2", E / "minish2.c"),
                      ("copy", L / "copy.c")]:
        subprocess.run(["gcc", "-std=c17", "-O2", "-Wall", "-Wextra", "-Werror", "-o",
                        str(d / name), str(src)], check=True)
    return d


def test_mycp_copies_bytes_and_mode(bins, tmp_path):
    data = bytes((i * 7) % 256 for i in range(70000))
    src = tmp_path / "src.bin"
    src.write_bytes(data)
    os.chmod(src, 0o751)
    for b in ["1", "7", "4096", "100000"]:
        dst = tmp_path / f"dst{b}"
        assert subprocess.run([str(bins / "mycp"), str(src), str(dst), b]).returncode == 0
        assert dst.read_bytes() == data and (dst.stat().st_mode & 0o7777) == 0o751
    again = subprocess.run([str(bins / "mycp"), str(src), str(tmp_path / "dst7")],
                           capture_output=True)
    assert again.returncode == 1                       # never overwrites


def test_tee(bins, tmp_path):
    a, b = tmp_path / "a.txt", tmp_path / "b.txt"
    text = "line one\nline two\n" * 1000
    p = subprocess.run([str(bins / "tee"), str(a), str(b)], input=text, capture_output=True,
                       text=True)
    assert p.stdout == text and a.read_text() == text and b.read_text() == text
    subprocess.run([str(bins / "tee"), "-a", str(a)], input="more\n", capture_output=True,
                   text=True)
    assert a.read_text() == text + "more\n"


def test_minish2(bins, tmp_path):
    script = ("echo b a c > in.txt\ntr -s _ _ < in.txt\nsort < in.txt\n"
              "echo 3 1 2 | tr _ _ | wc -w\nfalse | true\nsleep 0.2 &\nsleep 0.6\nexit\n")
    p = subprocess.run([str(bins / "minish2")], input=script, capture_output=True, text=True,
                       cwd=tmp_path, timeout=20)
    lines = [ln for ln in p.stdout.replace("minish2$ ", "\n").splitlines() if ln]
    assert lines == ["b a c", "b a c", "3", "[done: 1 background process]"]
    assert (tmp_path / "in.txt").read_text() == "b a c\n"


@pytest.mark.parametrize("n, b", [(100000, 1), (100000, 4096), (100000, 65536), (5, 10), (0, 8)])
def test_copy_law(bins, tmp_path, n, b):
    src = tmp_path / "in.txt"
    src.write_bytes(b"x" * n)
    log = tmp_path / "r.txt"
    subprocess.run(["strace", "-qq", "-e", "trace=read", "-P", str(src), "-o", str(log),
                    str(bins / "copy"), str(src), str(tmp_path / "out.txt"), str(b)], check=True)
    reads = len(log.read_text().splitlines())
    assert reads == -(-n // b) + 1                     # ceil(n / b) + 1
