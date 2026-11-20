"""fd_demo.py: the library's wide table under its dependencies: closures, keys,
a minimal cover, the BCNF decomposition and the 3NF synthesis."""
from fd import bcnf, closure, fds, is_3nf, keys, lossless, minimal_cover, preserves

WIDE = ("loan out due ret book title author genre pages member first last street"
        " postcode").split()
RULES = fds("loan -> book member out due ret; book -> title author genre pages;"
            " member -> first last street; street -> postcode")


def show(xs):
    return "{" + ", ".join(a for a in WIDE if a in xs) + "}"


if __name__ == "__main__":
    print("closure of {member}:", show(closure({"member"}, RULES)))
    print("closure of {book}:", show(closure({"book"}, RULES)))
    print("candidate keys:", [show(k) for k in keys(WIDE, RULES)])
    cover = minimal_cover(RULES)
    print(f"minimal cover: {len(cover)} dependencies, one attribute on each right side")
    print("in 3NF:", is_3nf(WIDE, RULES))
    parts = bcnf(WIDE, RULES)
    for p in parts:
        print("  BCNF table", show(p), "key", show(keys(p, RULES)[0]))
    print("lossless:", lossless(WIDE, parts, RULES), "| preserves the dependencies:",
          preserves(parts, RULES))
