"""exo_closure.py: attribute closures for the dependencies of exercise 1."""
from fd import closure, fds

DEPS = fds("a -> b; b c -> d; d -> e; e a -> c")
for xs in [{"a"}, {"b", "c"}, {"c", "e"}]:
    print(sorted(xs), "->", sorted(closure(xs, DEPS)))
