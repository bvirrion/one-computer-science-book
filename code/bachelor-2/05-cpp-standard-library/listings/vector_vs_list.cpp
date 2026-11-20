// vector_vs_list.cpp: n random values inserted in order, each position found by walking from the front.
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <list>
#include <random>
#include <vector>

template <class C> double fill_sorted(C &c, const std::vector<int> &values)   // milliseconds
{
    auto t0 = std::chrono::steady_clock::now();
    for (int x : values) {
        auto it = c.begin();
        while (it != c.end() && *it < x)               // linear search in both containers
            ++it;
        c.insert(it, x);                               // vector: shifts; list: links
    }
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

int main()
{
    std::mt19937 gen(2025);
    std::printf("%7s %11s %11s %7s\n", "n", "vector ms", "list ms", "ratio");
    for (int n : {1000, 2000, 5000, 10000, 20000, 40000}) {
        std::vector<int> values(n);
        for (int &x : values) x = int(gen() % 1000000);
        std::vector<int> v;
        std::list<int> l;
        double tv = fill_sorted(v, values), tl = fill_sorted(l, values);
        if (!std::equal(v.begin(), v.end(), l.begin())) return 1;
        std::printf("%7d %11.2f %11.2f %7.1f\n", n, tv, tl, tl / tv);
    }
    return 0;
}
