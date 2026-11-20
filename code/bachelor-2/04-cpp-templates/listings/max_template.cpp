// max_template.cpp: one function template, used with three types.
#include <iostream>
#include <string>

template <typename T>
const T &larger(const T &a, const T &b)
{
    return a < b ? b : a;
}

int main()
{
    std::cout << larger(3, 7) << '\n';                      // T = int
    std::cout << larger(2.5, -1.0) << '\n';                 // T = double
    std::string p = "pier", q = "dunes";
    std::cout << larger(p, q) << '\n';                      // T = std::string
    std::cout << larger<double>(3, 7.5) << '\n';            // T given: 3 converts to 3.0
    // larger(3, 7.5) does not compile: T would be int and double at once
    return 0;
}
