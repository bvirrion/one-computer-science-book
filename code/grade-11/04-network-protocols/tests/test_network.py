import importlib.util
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_addresses():
    ex = load("exercises", "net_ex")
    mb = load("listings", "mask_bits")
    import ipaddress
    for prefix in range(33):
        assert ipaddress.ip_network(f"0.0.0.0/{prefix}").netmask == \
            ipaddress.ip_address(mb.mask(prefix))
    assert ex.network_address("192.168.10.37/24") == "192.168.10.0"
    assert ex.hosts(26) == 62
    assert ex.same_network("192.0.2.37", "192.0.2.1", 26)
    assert not ex.same_network("192.0.2.37", "192.0.2.64", 26)
    assert ex.network_with_or("192.0.2.37", 26) == "255.255.255.229"
    assert ex.subnets("192.0.2.0/24", 4)[-1] == "192.0.2.192/26"


def test_routing():
    ex = load("exercises", "net_ex")
    rl = load("listings", "route_lookup")
    for a in ["192.0.2.99", "198.51.100.7", "198.51.100.200", "203.0.113.5"]:
        assert ex.lookup(rl.TABLE, a) == rl.lookup(a)[1]
    assert ex.lookup(rl.TABLE[:-1], "203.0.113.5") is None


def test_alternating_bit():
    from lossy_channel import Channel
    ab = load("listings", "alternating_bit")
    for seed in range(200):
        with redirect_stdout(io.StringIO()):
            got, sends = ab.run(list("abcdefgh"), Channel(0.4, seed), Channel(0.4, seed + 1))
        assert got == list("abcdefgh") and sends >= 8
    ex = load("exercises", "net_ex")
    assert ex.receiver([(0, "a"), (0, "a"), (1, "b")]) == ["a", "b"]
    assert ex.receiver([(0, "a"), (0, "a"), (1, "b")], check_bit=False) == ["a", "a", "b"]
    assert ex.receiver([(0, "a"), (1, "b"), (0, "a"), (0, "c")]) == ["a", "b", "a"]


def test_windows():
    ex = load("exercises", "net_ex")
    assert [ex.window_time(10, w, 4) for w in (1, 2, 5)] == [50, 26, 14]
    assert ex.window_time(10, 100, 4) == 14
