// deep_copy.cpp: each Buffer owns its block; copies are independent.
// capture: cflags=-O0 -g -fsanitize=address
#include <iostream>
#include "buffer.hpp"

int main()
{
    Buffer a("harbour Road");
    Buffer b = a;                    // copy constructor: a new block
    b.upcase_first();
    Buffer c("x");
    c = a;                           // copy assignment
    c = c;                           // self-assignment is harmless
    std::cout << a.c_str() << " / " << b.c_str() << " / " << c.c_str() << '\n';
    std::cout << "three blocks: " << std::boolalpha
              << (a.c_str() != b.c_str() && b.c_str() != c.c_str() && a.c_str() != c.c_str()) << '\n';
    return 0;
}
