// lru_test.cpp: the LRU cache of exercise 9 against a slow reference kept as a vector.
#include <algorithm>
#include <cassert>
#include <cstdio>
#include <random>
#include <string>
#include <vector>
#include "../exercises/lru.hpp"

int main()
{
    LruCache<std::string, int> c(2);
    c.put("Mill Row", 1);
    c.put("Quay Street", 2);
    assert(c.get("Mill Row") == 1);                 // Mill Row is now the most recent
    c.put("Bridge Way", 3);                         // evicts Quay Street
    assert(!c.get("Quay Street") && c.get("Mill Row") == 1 && c.get("Bridge Way") == 3 && c.size() == 2);

    std::mt19937 gen(7);
    for (std::size_t cap : {1u, 3u, 8u}) {
        LruCache<int, int> lru(cap);
        std::vector<std::pair<int, int>> ref;       // most recent first
        for (int step = 0; step < 5000; step++) {
            int k = int(gen() % 12), v = int(gen() % 100);
            auto it = std::find_if(ref.begin(), ref.end(), [k](auto p) { return p.first == k; });
            if (gen() % 2) {
                auto got = lru.get(k);
                assert(got.has_value() == (it != ref.end()));
                if (it != ref.end()) {
                    assert(*got == it->second);
                    auto p = *it;
                    ref.erase(it);
                    ref.insert(ref.begin(), p);
                }
            } else {
                lru.put(k, v);
                if (it != ref.end())
                    ref.erase(it);
                else if (ref.size() == cap)
                    ref.pop_back();
                ref.insert(ref.begin(), {k, v});
            }
            assert(lru.size() == ref.size());
        }
    }
    std::puts("lru_test: OK");
    return 0;
}
