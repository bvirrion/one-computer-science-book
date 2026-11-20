// with_concept.cpp: the same, with the requirement stated in front.
// capture: exit
#include <concepts>
#include <vector>

struct Point { double x, y; };

template <typename T>
concept Ordered = std::copyable<T> && requires(const T a, const T b) {
    { a < b } -> std::convertible_to<bool>;
};

template <Ordered T>
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
