// specialise.cpp: a general template and a version for one type.
#include <iostream>
#include <string>

template <typename T>
std::string describe(const T &x) { return "value " + std::to_string(x); }

template <>                                     // the full specialisation for bool
std::string describe<bool>(const bool &x) { return x ? "yes" : "no"; }

template <typename T>
std::string describe(T *p)
    { return p ? "pointer to " + describe(*p) : "null pointer"; }  // an overload

int main()
{
    int n = 42;
    bool open = true;
    std::cout << describe(n) << " | " << describe(2.5) << " | " << describe(open) << " | "
              << describe(&n) << " | " << describe(static_cast<int *>(nullptr)) << '\n';
    return 0;
}
