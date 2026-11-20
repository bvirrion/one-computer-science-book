import importlib.util
import io
import random
import sys
from collections import deque
from contextlib import redirect_stdout
from pathlib import Path

import pytest

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("name", ["queue_linked", "queue_two_stacks"])
def test_queues_against_deque(name):
    Queue = load("listings", name).Queue
    rng = random.Random(5)
    q, ref = Queue(), deque()
    for i in range(3000):
        if ref and rng.random() < 0.45:
            assert q.dequeue() == ref.popleft()
        else:
            q.enqueue(i)
            ref.append(i)
        assert q.is_empty() == (not ref)
    while ref:
        assert q.dequeue() == ref.popleft()


def test_two_stack_moves_bound():
    Queue = load("listings", "queue_two_stacks").Queue
    rng = random.Random(9)
    q, enq = Queue(), 0
    for i in range(2000):
        if not q.is_empty() and rng.random() < 0.5:
            q.dequeue()
        else:
            q.enqueue(i)
            enq += 1
        assert q.moves <= 3 * enq
    while not q.is_empty():
        q.dequeue()
    assert q.moves == 3 * enq


def test_brackets_and_postfix():
    b = load("listings", "brackets")
    rng = random.Random(1)
    for _ in range(2000):
        text = "".join(rng.choice("()[]") for _ in range(rng.randint(0, 8)))
        reduced = text
        while any(p in reduced for p in ("()", "[]")):
            reduced = reduced.replace("()", "").replace("[]", "")
        assert b.balanced(text) == (reduced == "")
    p = load("listings", "postfix")
    assert p.evaluate("5 1 2 + 4 * + 3 -") == 14


def test_post_office():
    po = load("listings", "post_office")
    a = po.simulate(load("listings", "queue_linked").Queue)
    b = po.simulate(load("listings", "queue_two_stacks").Queue)
    assert a[:3] == b[:3] == (114, 5, 13)
    assert (a[3], b[3]) == (228, 342)


def test_exercises():
    ex = load("exercises", "structures_ex")
    for S in (ex.SizedListStack, ex.SizedLinkedStack):
        s = S()
        s.push(1)
        s.push(2)
        s.pop()
        assert s.size() == 1
    cell = load("listings", "cell")
    head = cell.from_list([1, 2, 3, 4])
    assert ex.length_rec(head) == ex.length_iter(head) == 4
    assert cell.to_list(ex.reverse(head)) == [4, 3, 2, 1]
    assert ex.reverse(None) is None
    q = ex.BrokenQueue()
    q.enqueue(1)
    q.dequeue()
    q.enqueue(2)
    assert q._head is None
    c = ex.CircularQueue(3)
    for x in [1, 2, 3]:
        c.enqueue(x)
    with pytest.raises(OverflowError):
        c.enqueue(4)
    assert c.dequeue() == 1
    c.enqueue(4)
    assert [c.dequeue() for _ in range(3)] == [2, 3, 4]
    assert ex.to_postfix("( 2 + 3 ) * ( 7 - 4 ) / 5") == "2 3 + 7 4 - * 5 /"
    assert ex.to_postfix("10 - 2 - 3") == "10 2 - 3 -"
    p = load("listings", "postfix")
    assert p.evaluate(ex.to_postfix("1 + 2 * 3 - 8 / 4")) == 5
