// lambdas.cpp: generic algorithms, given their operation as a lambda expression.
#include <algorithm>
#include <cstdio>
#include <numeric>
#include <vector>

int main()
{
    std::vector<int> pages{65, 133, 412, 98, 251, 77, 320, 189};
    int limit = 150;                                        // a local variable, captured below
    auto is_long = [limit](int p) { return p > limit; };     // [limit]: a copy of limit
    long n_long = std::count_if(pages.begin(), pages.end(), is_long);
    auto first = std::find_if(pages.begin(), pages.end(), is_long);
    int total = std::accumulate(pages.begin(), pages.end(), 0);
    std::printf("%ld books over %d pages, the first at position %ld; %d pages in all\n",
        n_long, limit,
                first - pages.begin(), total);

    int calls = 0;
    auto counted = [&calls](int a, int b) { calls++; return a < b; };  // by reference
    std::sort(pages.begin(), pages.end(), counted);
    std::printf("sorted:");
    for (int p : pages)
        std::printf(" %d", p);
    std::printf("\n%d comparisons to sort 8 values\n", calls);

    auto it = std::lower_bound(pages.begin(), pages.end(), 200);               // binary search
    std::printf("first book of at least 200 pages: %d, at position %ld\n",
        *it, it - pages.begin());
    return 0;
}
