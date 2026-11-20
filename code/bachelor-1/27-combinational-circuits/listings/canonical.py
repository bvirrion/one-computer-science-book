"""canonical.py: the truth table of a Boolean function, its canonical sum of products
and product of sums; and how many functions of n variables there are."""

from itertools import product


def majority(a, b, c):
    return int(a + b + c >= 2)


def literal(name, value, positive):
    return name if value == positive else name + "'"


def sum_of_products(f, names):
    terms = []
    for row in product((0, 1), repeat=len(names)):
        if f(*row):  # a minterm: true on this row only
            terms.append("".join(literal(n, v, 1) for n, v in zip(names, row)))
    return " + ".join(terms)


def product_of_sums(f, names):
    factors = []
    for row in product((0, 1), repeat=len(names)):
        if not f(*row):  # a maxterm: false on this row only
            literals = [literal(n, v, 0) for n, v in zip(names, row)]
            factors.append("(" + " + ".join(literals) + ")")
    return "".join(factors)


if __name__ == "__main__":
    print("a b c | maj")
    for row in product((0, 1), repeat=3):
        print(*row, "|", majority(*row))
    print("sum of products:", sum_of_products(majority, "abc"))
    print("product of sums:", product_of_sums(majority, "abc"))
    print("functions of n variables:", [2 ** 2 ** n for n in range(1, 6)])
