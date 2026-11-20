// exo_algorithms.cpp: predict each line before running.
#include <algorithm>
#include <cstdio>
#include <numeric>
#include <vector>

int main()
{
    std::vector<int> v{4, 1, 4, 2, 4, 3};
    std::printf("a %ld\n", std::count(v.begin(), v.end(), 4));
    std::printf("b %ld\n", std::max_element(v.begin(), v.end()) - v.begin());
    std::vector<double> halves{0.5, 0.5, 0.5, 0.5};
    std::printf("c %g %g\n", double(std::accumulate(halves.begin(), halves.end(), 0)),
                std::accumulate(halves.begin(), halves.end(), 0.0));
    std::vector<int> w{1, 1, 2, 1, 1, 3, 3};
    auto end_unique = std::unique(w.begin(), w.end());
    std::printf("d %ld:", end_unique - w.begin());
    for (auto it = w.begin(); it != end_unique; ++it)
        std::printf(" %d", *it);
    auto end_kept = std::remove(v.begin(), v.end(), 4);
    std::printf("\ne %zu %ld\n", v.size(), end_kept - v.begin());
    v.erase(end_kept, v.end());
    std::printf("f %zu %d\n", v.size(), std::binary_search(v.begin(), v.end(), 3));
    return 0;
}
