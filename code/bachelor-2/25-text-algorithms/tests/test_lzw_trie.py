"""LZW decodes what it encodes; a^n takes the predicted number of codes; the trie."""
from hypothesis import given, settings
from hypothesis import strategies as st

from exo_lzw_an import formula
from lzw import decode, encode
from text_gen import archive, street_names
from trie import Trie


@settings(max_examples=500, deadline=None)
@given(st.binary(max_size=200) | st.text(alphabet="ab", max_size=200).map(str.encode))
def test_round_trip(data):
    assert decode(encode(data)) == data


def test_archive_round_trip():
    data = archive().encode()
    assert decode(encode(data)) == data


def test_a_n():
    assert all(len(encode(b"a" * n)) == formula(n) for n in range(1, 2000))


@settings(max_examples=200, deadline=None)
@given(st.lists(st.text(alphabet="abc ", max_size=8), max_size=20), st.text("abc", max_size=3))
def test_trie(words, prefix):
    t = Trie()
    for w in words:
        t.insert(w)
    assert t.words(prefix) == sorted({w for w in words if w.startswith(prefix)})
    assert all(w in t for w in words)


def test_streets():
    t = Trie()
    for name in street_names():
        t.insert(name)
    assert t.words("") == sorted(street_names())
