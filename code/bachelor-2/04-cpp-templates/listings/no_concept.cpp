// no_concept.cpp: a template used with a type that lacks what its body needs.
// capture: exit
#include <vector>

struct Point { double x, y; };                  // no operator<

template <typename T>
T smallest(const std::vector<T> &v)
{
    T best = v[0];
    for (const T &x : v)
        if (x < best)
            best = x;
    return best;
}

int main()
{
    std::vector<Point> pts = {{1, 2}, {0, 5}};
    Point p = smallest(pts);
    return int(p.x);
}
