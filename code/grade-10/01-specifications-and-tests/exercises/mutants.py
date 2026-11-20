import random
import re
from pathlib import Path

SOURCE = (Path(__file__).parent.parent / "listings" / "leap_fixed.py").read_text()
MUTATIONS = [("==", "!="), ("True", "False"), ("False", "True"),
             ("400", "100"), ("400", "4"), ("100", "400"), ("100", "4"),
             ("4 ", "100 "), ("4 ", "400 "), ("0:", "1:"), ("0\n", "1\n")]


def mutants():
    """Yield (description, source) for every one-place change of SOURCE."""
    body = SOURCE.index("    if")
    for old, new in MUTATIONS:
        for m in re.finditer(re.escape(old), SOURCE[body:]):
            i = body + m.start()
            line = SOURCE.count("\n", 0, i) + 1
            yield f"line {line}: {old.strip()} -> {new.strip()}", (
                SOURCE[:i] + new + SOURCE[i + len(old):])


def killed(source, years):
    space = {}
    exec(source, space)
    reference = {}
    exec(SOURCE, reference)
    return any(space["leap_year"](y) != reference["leap_year"](y) for y in years)



def main():
    boundary = [2024, 2023, 1900, 2000]
    rng = random.Random(2026)
    randoms = [rng.randint(1583, 2400) for _ in range(100)]
    all_mutants = list(mutants())
    print("mutants:", len(all_mutants))
    for name, suite in [("boundary suite (4 years)", boundary),
                        ("random suite (100 years)", randoms)]:
        survivors = [d for d, s in all_mutants if not killed(s, suite)]
        print(name, "kills", len(all_mutants) - len(survivors))
        for d in survivors:
            print("   survives:", d)


if __name__ == "__main__":
    main()
