// top_words.hpp: the k most frequent words, with std::partial_sort (exercise 3).
#pragma once
#include <algorithm>
#include <map>
#include <string>
#include <utility>
#include <vector>

inline std::vector<std::pair<std::string, int>> top_words(
    const std::map<std::string, int> &count, std::size_t k)
{
    std::vector<std::pair<std::string, int>> v(count.begin(), count.end());
    k = std::min(k, v.size());
    // the first k positions receive the k largest, in order; the rest are left in some order
    std::partial_sort(v.begin(), v.begin() + long(k), v.end(),
        [](const auto &a, const auto &b) {
        return a.second != b.second ? a.second > b.second : a.first < b.first;  // ties: a to z
    });
    v.resize(k);
    return v;
}
