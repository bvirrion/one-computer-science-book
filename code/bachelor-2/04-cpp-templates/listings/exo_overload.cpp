// exo_overload.cpp (exercise 1): an ordinary function, a template and an overload.
#include <cstdio>

void show(int) { std::puts("show(int)"); }
void show(double) { std::puts("show(double)"); }
template <typename T> void show(T) { std::puts("show<T>(T)"); }
template <typename T> void show(T *) { std::puts("show<T>(T *)"); }

int main()
{
    int n = 1;
    show(1);            // a
    show(1.5);          // b
    show(1.5f);         // c
    show('x');          // d
    show<int>(1);       // e
    show(&n);           // f
    show(nullptr);      // g
    return 0;
}
