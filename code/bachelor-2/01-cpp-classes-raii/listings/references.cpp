// references.cpp: references, const, overloading, a namespace, string and vector.
#include <iostream>
#include <string>
#include <vector>

namespace geometry {
double area(double side) { return side * side; }               // a square
double area(double w, double h) { return w * h; }              // a rectangle
}

void swap_ints(int &a, int &b)       // a and b are other names for the caller's ints
{
    int t = a;
    a = b;
    b = t;
}

int total_length(const std::vector<std::string> &words)   // read-only, not copied
{
    int n = 0;
    for (const std::string &w : words)
        n += static_cast<int>(w.size());
    return n;
}

int main()
{
    int x = 1, y = 2;
    int &r = x;                      // r is x, from now on
    r = 10;
    swap_ints(x, y);
    std::cout << "x = " << x << ", y = " << y << '\n';
    std::cout << geometry::area(3.0) << ' ' << geometry::area(2.0, 4.5) << '\n';
    std::vector<std::string> streets{"Mill Lane", "Harbour Road", "Station Street"};
    streets.push_back("Elm Row");
    std::cout << streets.size() << " streets, " << total_length(streets) << " letters\n";
    return 0;
}
