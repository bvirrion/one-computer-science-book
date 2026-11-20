"""ex6_delete.py -- deletion from the B+ tree of bptree.py. A node left below its
minimum (a leaf with fewer than ceil((m-1)/2) keys, an internal node with fewer than
ceil(m/2) children) borrows from a sibling that can spare one, or else merges with a
sibling; a root left with one child is replaced by it."""

from bisect import bisect_left, bisect_right


def too_small(t, n):
    m = t.m
    return len(n.keys) < m // 2 if n.leaf else len(n.kids) < (m + 1) // 2


def can_spare(t, n):
    """Still at its minimum after giving one entry away?"""
    m = t.m
    return len(n.keys) - 1 >= m // 2 if n.leaf else len(n.kids) - 1 >= (m + 1) // 2


def delete(t, key):
    _delete(t, t.root, key)
    root = t.nodes[t.root]
    if not root.leaf and len(root.kids) == 1:
        t.root = root.kids[0]


def _delete(t, pid, key):
    n = t.node(pid)
    if n.leaf:
        i = bisect_left(n.keys, key)
        if i < len(n.keys) and n.keys[i] == key:
            del n.keys[i], n.kids[i]
        return
    i = bisect_right(n.keys, key)
    _delete(t, n.kids[i], key)
    if too_small(t, t.nodes[n.kids[i]]):
        repair(t, n, i)


def repair(t, parent, i):
    c = t.nodes[parent.kids[i]]
    left = t.nodes[parent.kids[i - 1]] if i > 0 else None
    right = t.nodes[parent.kids[i + 1]] if i + 1 < len(parent.kids) else None
    for sib, side in ((left, -1), (right, 1)):
        if sib is not None and can_spare(t, sib):
            borrow(parent, i, c, sib, side)
            return
    j = i - 1 if left is not None else i  # merge kids j and j + 1
    a, b = t.nodes[parent.kids[j]], t.nodes[parent.kids[j + 1]]
    if a.leaf:
        a.keys += b.keys
        a.kids += b.kids
        a.next = b.next
    else:
        a.keys += [parent.keys[j]] + b.keys
        a.kids += b.kids
    del parent.keys[j], parent.kids[j + 1]


def borrow(parent, i, c, sib, side):
    if side < 0:  # from the left sibling
        if c.leaf:
            c.keys.insert(0, sib.keys.pop())
            c.kids.insert(0, sib.kids.pop())
            parent.keys[i - 1] = c.keys[0]
        else:
            c.keys.insert(0, parent.keys[i - 1])
            c.kids.insert(0, sib.kids.pop())
            parent.keys[i - 1] = sib.keys.pop()
    else:  # from the right sibling
        if c.leaf:
            c.keys.append(sib.keys.pop(0))
            c.kids.append(sib.kids.pop(0))
            parent.keys[i] = sib.keys[0]
        else:
            c.keys.append(parent.keys[i])
            c.kids.append(sib.kids.pop(0))
            parent.keys[i] = sib.keys.pop(0)
