"""Window limits: the staged failure, the estimator, the state machine, AIMD."""
import math

import aimd
import fairness
import go_back_n
import rto
import selective_repeat
import tcp_states


def test_sr_too_wide_takes_old_packet(capsys):
    import sr_too_wide  # noqa: F401
    assert "'packet 3', 'packet 0']" in capsys.readouterr().out


def test_sr_limit_rejects_old_packet():
    r = selective_repeat.Receiver(k=2, window=2)
    sent = []
    r.link = type("L", (), {"send": lambda self, s: sent.append(s)})()
    r.clock = type("C", (), {"now": 0.0})()
    r.on_packet((0, "a"))
    r.on_packet((1, "b"))
    r.on_packet((0, "a"))                        # a resent old packet
    assert r.out == ["a", "b"] and r.buffer == {} and sent == [0, 1, 0]


def test_window_asserts():
    import pytest
    with pytest.raises(AssertionError):
        go_back_n.transfer([1], k=3, window=8)
    with pytest.raises(AssertionError):
        selective_repeat.transfer([1], k=3, window=5)


def test_rto_rules():
    rows = list(rto.estimate([800, 800]))
    assert rows[0][1:4] == (800, 400, 2400)
    assert rows[1][2] == 300 and rows[1][3] == 2000
    assert all(r[4] >= 1000 for r in rto.estimate([10, 20, 30]))


def test_tcp_states_close_both_ways(capsys):
    a = tcp_states.run("a", ["close", "receive FIN", "receive ACK", "2 MSL pass"], "ESTABLISHED")
    b = tcp_states.run("b", ["receive FIN", "close", "receive ACK"], "ESTABLISHED")
    assert a == b == "CLOSED"


def test_aimd_law_small_p():
    for p in (0.001, 0.0003):
        per = sum(int(w) for w in aimd.rounds(200_000, p)) / 200_000
        assert abs(per / math.sqrt(3 / (2 * p)) - 1) < 0.03


def test_aimd_fair_mimd_not():
    *_, last = fairness.trajectory(4.0, 40.0, 50.0, 400)
    assert fairness.jain(last) > 0.999
    *_, last = fairness.trajectory(4.0, 40.0, 50.0, 400, increase=0, decrease=0.5)
    *_, mimd = mimd_run(4.0, 40.0)
    assert abs(mimd[1] / mimd[0] - 10) < 1e-9


def mimd_run(x1, x2, capacity=50.0, n=400):
    for _ in range(n):
        yield x1, x2
        if x1 + x2 > capacity:
            x1, x2 = x1 / 2, x2 / 2
        else:
            x1, x2 = x1 * 1.1, x2 * 1.1
