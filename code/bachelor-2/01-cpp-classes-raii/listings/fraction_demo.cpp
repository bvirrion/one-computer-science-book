// fraction_demo.cpp: every Fraction is in lowest terms with a positive denominator.
#include <iostream>
#include <stdexcept>
#include "fraction.hpp"

std::ostream &operator<<(std::ostream &out, const Fraction &f)
{
    return out << f.num() << '/' << f.den();
}

int main()
{
    Fraction a(6, -8);
    Fraction b(1, 4);
    std::cout << "a = " << a << ", b = " << b << '\n';
    std::cout << "a + b = " << a + b << ", a * b = " << a * b << '\n';
    std::cout << "a + 1 = " << a + 1 << '\n';
    std::cout << std::boolalpha << "2/4 == 1/2: "
        << (Fraction(2, 4) == Fraction(1, 2)) << '\n';
    try {
        Fraction bad(3, 0);
        std::cout << "never printed " << bad << '\n';
    } catch (const std::invalid_argument &e) {
        std::cout << "refused: " << e.what() << '\n';
    }
    return 0;
}
