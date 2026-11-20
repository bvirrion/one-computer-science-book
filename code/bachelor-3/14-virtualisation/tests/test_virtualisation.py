import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE.parent / "listings"), str(HERE.parent / "exercises"),
                str(ROOT / "code" / "shared" / "rv")]

import ex6_timer  # noqa: E402
import ex11_detect  # noqa: E402
import ex12_fence  # noqa: E402
import nested_walk  # noqa: E402
from ex5_stuck import StuckMonitor  # noqa: E402
from monitor import Monitor  # noqa: E402
from rv import Machine, RVFault, StepLimit  # noqa: E402

GUEST = (HERE.parent / "listings" / "guest.S").read_text()


def csr(funct3, rd, number, rs1):
    return f".word 0x{number << 20 | rs1 << 15 | funct3 << 12 | rd << 7 | 0x73:08x}"


def test_bare_machine_refuses_the_guest():
    with pytest.raises(RVFault, match="illegal instruction"):
        Machine(GUEST).run()


def test_guest_under_the_monitor_and_exercise_4():
    vm = Monitor(GUEST)
    console, status = vm.run()
    assert console.startswith("hello from the guest\n5050\n") and status == 0
    # exercise 4: one trap per character, then show, read, show, power off
    assert vm.m.traps == len("hello from the guest\n") + 4


def test_exercise_5_stuck_monitor_loops():
    vm = StuckMonitor(GUEST)
    with pytest.raises(StepLimit):
        vm.m.run(1000)
    assert vm.console == ["h"] * vm.m.traps and vm.m.traps > 900


def test_exercise_6_timer_fires_once():
    a0, t0 = 10, 5
    src = "\n".join([
        "main: la a0, handler", csr(1, 0, 0x5C5, a0),
        "li a0, 50", csr(1, 0, 0x5C4, a0),
        "li t1, 0",
        "spin: addi t1, t1, 1", "j spin",
        "handler: mv a0, t1", csr(1, 0, 0x5C3, a0),
        csr(2, t0, 0x5C6, 0), "mv a0, t0", csr(1, 0, 0x5C3, a0),
        "li a0, 0", csr(1, 0, 0x5C1, a0)])
    vm = ex6_timer.TimerMonitor(src)
    console, status = vm.run()
    count, epc = (int(v) for v in console.split())
    # 6 instructions before the loop (la is two), then 2 per round
    assert count == (50 - 6) // 2 and status == 0
    assert epc in (vm.m.prog.symbols["spin"], vm.m.prog.symbols["spin"] + 4)
    assert vm.timer[ex6_timer.TIMECMP] == 0


def test_exercise_7_walk_count():
    for k in range(1, 7):
        for h in range(1, 7):
            assert len(nested_walk.two_stage(k, h)) - 1 == k * h + k + h
        assert len(nested_walk.two_stage(k, k)) - 1 == (k + 1) ** 2 - 1


def test_exercise_11_timing_detects_the_monitor():
    for charge in (0, 1, 50):
        vm = ex11_detect.ChargingMonitor(ex11_detect.GUEST, charge)
        console, _ = vm.run()
        assert int(console) == charge


def test_exercise_12_fence():
    inside = "main: li t0, 0x10000000\nsw t0, 0(t0)\nlw t1, 0(t0)\nli a0, 0\nret"
    m = Machine(inside + "\n.data\nslot: .word 0")
    while not m.halted:
        ex12_fence.checked_step(m, 0x10000000, 0x10000004)
    outside = inside.replace("sw t0, 0(t0)", "sw t0, 4(t0)")
    m = Machine(outside + "\n.data\nslot: .word 0, 0")
    with pytest.raises(RVFault, match="outside"):
        while not m.halted:
            ex12_fence.checked_step(m, 0x10000000, 0x10000004)
    assert m.load(0x10000004, 4) == 0  # stopped before the store
