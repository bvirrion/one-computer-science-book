"""The switch learns, forwards, floods and filters; ARP caches; the two-switch line."""
import arp_sim
from switch_sim import Switch


def test_switch_rules():
    sw = Switch([1, 2, 3])
    assert sw.receive("A", "B", 1) == [2, 3]          # unknown: flood
    assert sw.receive("B", "A", 2) == [1]             # learned: forward
    assert sw.receive("C", "A", 1) == []              # same port: filter
    assert sw.table == {"A": 1, "B": 2, "C": 1}


def test_arp_cache_expires(capsys):
    a = arp_sim.Host("A", "10.0.0.1", "m1")
    c = arp_sim.Host("C", "10.0.0.3", "m3")
    arp_sim.send([a, c], a, "10.0.0.3", 0)
    assert a.lookup("10.0.0.3", 59) == "m3" and c.lookup("10.0.0.1", 1) == "m1"
    assert a.lookup("10.0.0.3", 60) is None
    assert "broadcast" in capsys.readouterr().out


def test_two_switches(capsys):
    import exo_switch                                 # runs the six frames
    assert exo_switch.s1.table == {"A": 1, "B": 2, "C": 3, "D": 3}
    assert exo_switch.s2.table == {"A": 1, "B": 1, "C": 2, "D": 3}
