// ranges.cpp: the same questions with C++20 ranges: whole containers, and views composed with |.
#include <algorithm>
#include <cstdio>
#include <ranges>
#include <vector>

int main()
{
    std::vector<int> pages{65, 133, 412, 98, 251, 77, 320, 189};
    namespace views = std::views;
    std::ranges::sort(pages);                                   // no begin() and end() to pass
    auto long_ones = pages | views::filter([](int p) { return p > 150; })
                           | views::transform([](int p) { return p / 10; });  // not run yet
    std::printf("tens of pages of the long books:");
    for (int t : long_ones)                              // computed now, one element at a time
        std::printf(" %d", t);
    std::printf("\nthree largest:");
    for (int p : pages | views::reverse | views::take(3))
        std::printf(" %d", p);
    std::printf("\n%s\n", std::ranges::is_sorted(pages) ? "sorted" : "not sorted");
    return 0;
}
