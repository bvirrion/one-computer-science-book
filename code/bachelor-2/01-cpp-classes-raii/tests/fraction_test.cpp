// fraction_test.cpp: the invariant holds after every constructor and operator.
#include <cassert>
#include <cstdio>
#include <numeric>
#include <stdexcept>
#include "fraction.hpp"

static void invariant(const Fraction &f)
{
    assert(f.den() > 0);
    assert(std::gcd(f.num(), f.den()) == 1);
}

int main()
{
    for (long a = -12; a <= 12; a++)
        for (long b = -12; b <= 12; b++) {
            if (b == 0) {
                bool refused = false;
                try { Fraction(a, b); } catch (const std::invalid_argument &) { refused = true; }
                assert(refused);
                continue;
            }
            Fraction f(a, b);
            invariant(f);
            assert(f.num() * b == a * f.den());          // same rational number
            Fraction s = f + Fraction(1, 3), p = f * Fraction(-2, 5);
            invariant(s);
            invariant(p);
            assert(s.num() * 3 * b == (3 * a + b) * s.den());
            assert(p.num() * 5 * b == -2 * a * p.den());
        }
    assert(Fraction(6, -8) == Fraction(-3, 4));
    assert(Fraction(0, -5) == Fraction(0));
    std::puts("fraction_test: ok");
    return 0;
}
