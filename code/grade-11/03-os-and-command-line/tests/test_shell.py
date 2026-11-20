import importlib.util
import io
import shutil
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
TOWN = HERE.parents[2] / "data" / "town"
sys.path.insert(0, str(HERE / "listings"))


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / "listings" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()) as out:
        spec.loader.exec_module(module)
    return module, out.getvalue()


def bash(cmd, cwd):
    return subprocess.run(["bash", "-c", cmd], cwd=cwd, capture_output=True, text=True)


def test_pipelines(tmp_path):
    for name in ("books.csv", "loans.csv"):
        shutil.copy(TOWN / name, tmp_path)
    out = bash(f"bash {HERE / 'exercises' / 'pipelines.sh'}", tmp_path).stdout.split("\n")
    assert out[0].strip() == "80"
    assert [line.split(maxsplit=1)[1] for line in out[1:4]] == \
        ["Elif Ashworth", "Quinn Ivymore", "Zoe Stoneton"]
    assert out[4:6] == ["9", "80"]
    count = bash(f"bash {HERE / 'exercises' / 'count_loans.sh'} 55", tmp_path).stdout
    assert count.strip() == "12"
    assert bash(f"bash {HERE / 'exercises' / 'count_loans.sh'}", tmp_path).returncode == 1


def test_shell_traps(tmp_path):
    (tmp_path / "f.txt").write_text("hello\n")
    bash("cat f.txt > f.txt", tmp_path)
    assert (tmp_path / "f.txt").read_text() == ""
    (tmp_path / "My Notes").mkdir()
    assert bash("cd My Notes", tmp_path).returncode != 0
    assert bash('cd "My Notes"', tmp_path).returncode == 0
    bash("echo a >> g.txt; echo b >> g.txt", tmp_path)
    assert (tmp_path / "g.txt").read_text() == "a\nb\n"


def test_modes():
    assert sum(1 for m in range(512) if m & 0o002) == 256
    t, _ = load("timetable")
    assert t.can("chloe", "/school/timetable.txt", 2)
    assert t.can("dev", "/school/marks/g11.csv", 4)
    assert not t.can("dev", "/school/marks/g11.csv", 2)


def test_policy():
    _, text = load("policy")
    assert "bits changed in all: 8" in text
    assert "/school/marks/g11.csv  644 -> 660  (8 mode(s) fit, 2 bits changed)" in text
