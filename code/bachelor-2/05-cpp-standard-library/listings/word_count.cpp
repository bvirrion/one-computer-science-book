// word_count.cpp: the most frequent words in the titles of the town's books, read from standard input.
#include <cstdio>
#include <iostream>
#include "words.hpp"

int main()
{
    auto count = count_words(std::cin);
    auto top = by_frequency(count);
    int total = 0;
    for (const auto &[w, n] : count)
        total += n;
    std::printf("%d words, %zu different\n", total, count.size());
    for (std::size_t i = 0; i < 8; i++)
        std::printf("%-8s %d\n", top[i].first.c_str(), top[i].second);
    return 0;
}
