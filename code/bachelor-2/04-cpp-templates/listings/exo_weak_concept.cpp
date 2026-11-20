// exo_weak_concept.cpp (exercise 6): the concept is satisfied, and still an error.
// capture: exit
#include <concepts>
#include <string>
#include <vector>

template <typename T>
concept Ordered = requires(const T a, const T b) { { a < b } -> std::convertible_to<bool>; };

template <Ordered T>
T middle(const std::vector<T> &v)           // the mean of the smallest and the largest
{
    T lo = v[0], hi = v[0];
    for (const T &x : v) {
        if (x < lo) lo = x;
        if (hi < x) hi = x;
    }
    return (lo + hi) / 2;
}

int main()
{
    std::vector<double> d = {3.5, 1.0, 8.0};
    std::vector<std::string> s = {"pier", "dunes"};
    double m = middle(d);
    std::string t = middle(s);
    return int(m) + int(t.size());
}
