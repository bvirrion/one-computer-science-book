"""laws.py: two laws of relational algebra checked on random relations, and what
pushing a selection below a join saves on the town's tables."""

import random

from algebra import Relation, natural_join, project, select, table, union


def random_relation(schema, rng, n=8, values=4):
    return Relation(schema, [tuple(rng.randrange(values) for _ in schema)
                             for _ in range(rng.randrange(n))])


def check_laws(trials=2000, seed=29):
    rng = random.Random(seed)
    for _ in range(trials):
        r, r2 = random_relation("ab", rng), random_relation("ab", rng)
        s = random_relation("bc", rng)
        k = rng.randrange(4)
        def c(t, k=k):
            return t["a"] == k  # mentions only attributes of r
        assert select(union(r, r2), c) == union(select(r, c), select(r2, c))
        assert select(natural_join(r, s), c) == natural_join(select(r, c), s)
    return trials


if __name__ == "__main__":
    print("sigma over union, sigma through a join:", check_laws(),
          "random cases, all equal")
    loans, books = table("loans"), table("books")
    def poetry(t):
        return t["genre"] == "poetry"
    joined = natural_join(loans, books)
    late = select(joined, poetry)
    pushed = natural_join(loans, select(books, poetry))
    print(f"select after the join: join builds {len(joined)} tuples, "
          f"keeps {len(late)}")
    print(f"select pushed down: select keeps {len(select(books, poetry))} books, "
          f"join builds {len(pushed)} tuples")
    readers = project(late, ("member_id",))
    print("same answer:", late == pushed, "| poetry readers:", len(readers))
