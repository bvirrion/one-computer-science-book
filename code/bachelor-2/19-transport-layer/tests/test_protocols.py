"""Every protocol delivers the exact stream under loss, duplication and reordering."""
from hypothesis import given, settings
from hypothesis import strategies as st

import go_back_n
import selective_repeat
import stop_and_wait

seeds = st.integers(0, 10**6)
DATA = list(range(300))


@settings(max_examples=25, deadline=None)
@given(seeds, st.sampled_from([0.0, 0.1, 0.3]), st.sampled_from([0.0, 0.1]))
def test_stop_and_wait(seed, loss, dup):
    out, _, _ = stop_and_wait.transfer(DATA, loss=loss, dup=dup, seed=seed)
    assert out == DATA


@settings(max_examples=25, deadline=None)
@given(seeds, st.integers(2, 5), st.sampled_from([0.0, 0.1, 0.3]))
def test_gbn_full_window_fifo(seed, k, loss):
    out, _, _ = go_back_n.transfer(DATA, k=k, window=2**k - 1, loss=loss, dup=0.1, seed=seed)
    assert out == DATA


@settings(max_examples=25, deadline=None)
@given(seeds, st.integers(2, 6), st.sampled_from([0.0, 0.1, 0.3]))
def test_sr_full_window_fifo(seed, k, loss):
    w = 2 ** (k - 1)
    out, _, _ = selective_repeat.transfer(DATA, k=k, window=w, loss=loss, dup=0.1, seed=seed)
    assert out == DATA


@settings(max_examples=25, deadline=None)
@given(seeds, st.sampled_from([0.0, 0.2]))
def test_reordering_with_room(seed, loss):
    # jitter of 10 ms reorders up to about 10 packets; the sequence space leaves room
    kw = dict(loss=loss, dup=0.05, jitter=10, seed=seed)
    assert go_back_n.transfer(DATA, k=8, window=31, **kw)[0] == DATA
    assert selective_repeat.transfer(DATA, k=8, window=31, **kw)[0] == DATA


def test_file_copy_and_fast_retransmit(capsys):
    import fast_retransmit  # noqa: F401
    import file_copy  # noqa: F401
    out = capsys.readouterr().out
    assert "identical to the original: True" in out
    assert out.count("intact True") == 2
