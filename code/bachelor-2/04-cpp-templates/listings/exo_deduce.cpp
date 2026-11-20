// exo_deduce.cpp (exercise 5): three calls of function templates.
// capture: exit
#include <string>

template <typename T> T larger(T a, T b) { return a < b ? b : a; }
template <typename T> T parse(const std::string &s) { return T(s.size()); }

int main()
{
    int a = larger(3, 7.5);                 // 1
    auto n = parse("12");                   // 2
    std::string s = larger("pier", "dunes rd");   // 3
    return a + int(n) + int(s.size());
}
