// exo_order.cpp: predict every line.
#include <iostream>
#include "noisy.hpp"

Noisy g("global");

void f(int k)
{
    Noisy x("x" + std::to_string(k));
    if (k > 0)
        f(k - 1);
}

int main()
{
    Noisy a("a");
    f(1);
    {
        Noisy b("b");
    }
    return 0;
}
