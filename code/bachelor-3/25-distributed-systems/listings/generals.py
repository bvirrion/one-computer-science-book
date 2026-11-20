"""generals.py -- the two generals with k messengers. General A sends messenger 1 to B;
whoever receives messenger j sends messenger j + 1 back, up to k. A messenger may be
captured; then nothing more is sent. A general's whole knowledge is how many
messengers reached it, so a protocol is a pair of rules: messengers received ->
attack or not. B cannot attack before it has heard the plan. Every pair of rules is
tried against every run."""

from itertools import product


def runs(k):
    """(messengers received by A, by B) when messenger `lost` is captured."""
    for lost in range(1, k + 2):
        delivered = lost - 1
        yield lost, delivered // 2, (delivered + 1) // 2


def rules(views):
    """Every function from range(views) to {False, True}, as a tuple."""
    return product((False, True), repeat=views)


def check(k):
    agree_always = useful = 0
    for a, b in product(rules(k // 2 + 1), rules((k + 1) // 2 + 1)):
        if b[0]:  # B attacks without having heard of the plan
            continue
        ok = all(a[ra] == b[rb] for _, ra, rb in runs(k))
        attack_if_all_arrive = a[k // 2] and b[(k + 1) // 2]
        agree_always += ok
        useful += ok and attack_if_all_arrive
    return agree_always, useful


if __name__ == "__main__":
    print(" k  protocols  always agree  and attack when no messenger is lost")
    for k in range(1, 9):
        n = 2 ** (k // 2 + 1) * 2 ** ((k + 1) // 2)
        agree, useful = check(k)
        print(f"{k:>2} {n:>10} {agree:>13} {useful:>15}")
