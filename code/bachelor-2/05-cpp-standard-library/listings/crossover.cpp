// crossover.cpp: n random keys inserted, then each looked up once: a sorted vector against a map.
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <map>
#include <random>
#include <vector>

template <class F> double ns_per_key(int n, F f)
{
    auto t0 = std::chrono::steady_clock::now();
    if (f() != n) return -1;                                   // every key must be found
    return std::chrono::duration<double, std::nano>(std::chrono::steady_clock::now() - t0).count() / n;
}

int main()
{
    std::mt19937 gen(2025);
    std::printf("%7s %14s %8s\n", "n", "sorted vector", "map");
    for (int size = 1000; size <= 128000; size *= 2) {
        std::vector<int> keys(size);
        for (int &k : keys) k = int(gen() >> 1);               // distinct with high probability
        std::sort(keys.begin(), keys.end());
        keys.erase(std::unique(keys.begin(), keys.end()), keys.end());
        int n = int(keys.size());
        std::shuffle(keys.begin(), keys.end(), gen);
        double tv = ns_per_key(n, [&] {
            std::vector<int> v;
            for (int k : keys) v.insert(std::lower_bound(v.begin(), v.end(), k), k);   // shifts the tail
            int found = 0;
            for (int k : keys) found += std::binary_search(v.begin(), v.end(), k);
            return found;
        });
        double tm = ns_per_key(n, [&] {
            std::map<int, int> m;
            for (int k : keys) m.emplace(k, 0);                                        // allocates a node
            int found = 0;
            for (int k : keys) found += int(m.count(k));
            return found;
        });
        std::printf("%7d %14.1f %8.1f\n", n, tv, tm);
    }
    return 0;
}
