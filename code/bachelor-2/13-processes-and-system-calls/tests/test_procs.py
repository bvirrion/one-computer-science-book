"""End-to-end: the shell on scripts, the fork tree, runit, xargs_lite and ptree."""
import subprocess
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent.parent
L, E = HERE / "listings", HERE / "exercises"


@pytest.fixture(scope="module")
def build(tmp_path_factory):
    d = tmp_path_factory.mktemp("bin")
    progs = {"minish": [L / "minish.c", L / "minish_parse.c"], "fork_tree": [L / "fork_tree.c"],
             "runit": [E / "runit.c"], "xargs_lite": [E / "xargs_lite.c"], "ptree": [E / "ptree.c"]}
    for name, srcs in progs.items():
        subprocess.run(["gcc", "-std=c17", "-O2", "-Wall", "-Wextra", "-Werror", "-I", str(L),
                        "-o", str(d / name), *map(str, srcs)], check=True)
    return d


def shell(build, script, cwd="/"):
    p = subprocess.run([str(build / "minish")], input=script, capture_output=True, text=True,
                       cwd=cwd, env={"PATH": "/usr/bin:/bin", "HOME": "/tmp"}, timeout=20)
    return p.returncode, p.stdout, p.stderr


def test_shell_runs_commands_and_keeps_status(build):
    rc, out, err = shell(build, "echo one two\nfalse\necho $?\nno-such-cmd\necho $?\n")
    assert rc == 0
    lines = [ln for ln in out.splitlines() if not ln.startswith("minish$")]
    assert lines == ["one two", "1", "127"]
    assert "command not found" in err


def test_cd_is_built_in(build):
    rc, out, _ = shell(build, "cd /usr\npwd\ncd\npwd\ncd /nowhere\necho $?\n")
    lines = [ln for ln in out.splitlines() if not ln.startswith("minish$")]
    assert lines == ["/usr", "/tmp", "1"]


def test_exit_status_and_signal(build):
    assert shell(build, "exit 7\necho never\n")[0] == 7
    assert shell(build, "false\n")[0] == 1                     # end of input: the last status
    assert shell(build, "true\n")[0] == 0


def test_fork_count(build):
    out = subprocess.run([str(build / "fork_tree")], capture_output=True, text=True).stdout
    names = [ln.split()[0] for ln in out.splitlines()]
    assert len(names) == 2 ** 3 and len(set(names)) == 8          # 3 forks: 8 processes
    assert sorted(len(n) - 1 for n in names) == [0, 1, 1, 1, 2, 2, 2, 3]


def test_runit(build):
    def run(*a):
        return subprocess.run([str(build / "runit"), *a], capture_output=True).returncode

    assert run("true") == 0 and run("false") == 1 and run("sh", "-c", "exit 42") == 42
    assert run("sh", "-c", "kill $$") == 128 + 15 and run("no-such-command") == 127


def test_xargs_lite(build):
    p = subprocess.run([str(build / "xargs_lite"), "2", "echo", "X"], input="a b c\nd e\n",
                       capture_output=True, text=True)
    assert p.stdout == "X a b\nX c d\nX e\n" and p.returncode == 0
    p = subprocess.run([str(build / "xargs_lite"), "3", "sh", "-c", 'exit "$#"', "sh"],
                       input="1 2 3 4", capture_output=True, text=True)
    assert p.returncode == 3                                       # the worst status: 3, then 1


def test_ptree(build):
    out = subprocess.run([str(build / "ptree")], capture_output=True, text=True, timeout=20).stdout
    assert out == "ptree\n  child-a\n    grandchild\n    grandchild\n  child-b\n"
