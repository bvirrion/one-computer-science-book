// lifetimes.cpp: automatic objects die at the end of their scope, last made first.
#include <iostream>
#include "noisy.hpp"

void visit()
{
    Noisy c("c (in visit)");
    std::cout << "  visit returns\n";
}

int main()
{
    std::cout << "main starts\n";
    Noisy a("a");
    {
        Noisy b1("b1");
        Noisy b2("b2");
        visit();
        std::cout << "  inner scope ends\n";
    }
    for (int i = 0; i < 2; i++) {
        Noisy d("d" + std::to_string(i));
    }
    std::cout << "main returns\n";
    return 0;
}
