// map_vs_unordered.cpp: nanoseconds per successful lookup in three structures holding the same n keys.
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <map>
#include <random>
#include <unordered_map>
#include <vector>

template <class Has> double ns_per_lookup(const std::vector<int> &keys, Has has)
{
    const long q = 2000000;                                    // the same number of lookups for every n
    long found = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (long i = 0; i < q; i++)
        found += has(keys[std::size_t(i) % keys.size()]);
    double ns = std::chrono::duration<double, std::nano>(std::chrono::steady_clock::now() - t0).count();
    return found == q ? ns / q : -1;                           // -1: a lookup failed
}

int main()
{
    std::mt19937 gen(2025);
    std::printf("%9s %14s %8s %14s\n", "n", "sorted vector", "map", "unordered_map");
    for (int n = 1000; n <= 1000000; n *= 10) {
        std::vector<int> keys(n);
        for (int &k : keys) k = int(gen());
        std::vector<int> sorted = keys;
        std::sort(sorted.begin(), sorted.end());
        std::map<int, int> m;
        std::unordered_map<int, int> u;
        for (int k : keys) m[k] = 1, u[k] = 1;
        std::shuffle(keys.begin(), keys.end(), gen);           // look the keys up in another order
        double tv = ns_per_lookup(keys, [&](int k) { return std::binary_search(sorted.begin(), sorted.end(), k); });
        double tm = ns_per_lookup(keys, [&](int k) { return m.count(k); });
        double tu = ns_per_lookup(keys, [&](int k) { return u.count(k); });
        std::printf("%9d %14.1f %8.1f %14.1f\n", n, tv, tm, tu);
    }
    return 0;
}
