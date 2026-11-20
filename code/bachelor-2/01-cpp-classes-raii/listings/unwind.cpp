// unwind.cpp: a throw three calls deep; every object on the way is destroyed.
#include <iostream>
#include <stdexcept>
#include "noisy.hpp"

void parse(int depth)
{
    Noisy n("p" + std::to_string(depth));
    if (depth == 3)
        throw std::runtime_error("bad record at depth 3");
    parse(depth + 1);
    std::cout << "  never printed\n";
}

int main()
{
    Noisy m("m");
    try {
        Noisy t("t");
        parse(1);
    } catch (const std::runtime_error &e) {
        std::cout << "caught: " << e.what() << '\n';
    }
    std::cout << "main goes on\n";
    return 0;
}
