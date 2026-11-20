// word_count_test.cpp: the word counts of the town's titles, checked against a count by hand of a small file.
#include <cassert>
#include <cstdio>
#include <fstream>
#include <sstream>
#include "words.hpp"
#include "../exercises/top_words.hpp"

int main()
{
    std::istringstream small("book_id,title,author\n1,The Silent Code,X\n2,the code of the Forest,Y\n");
    auto c = count_words(small);
    assert(c.size() == 5 && c["the"] == 3 && c["code"] == 2 && c["silent"] == 1 && c["of"] == 1);
    auto top = by_frequency(c);
    assert(top[0].first == "the" && top[1].first == "code" && top[2].first == "forest");  // ties alphabetical

    std::ifstream in("../../../../data/town/books.csv");
    auto town = count_words(in);
    int total = 0;
    for (const auto &[w, n] : town)
        total += n;
    assert(total == 262 && town.size() == 33 && town["the"] == 72);
    auto t3 = top_words(town, 3);                   // exercise 3 agrees with the full sort
    auto all = by_frequency(town);
    assert(t3.size() == 3);
    for (std::size_t i = 0; i < 3; i++)
        assert(t3[i] == all[i]);
    assert(top_words(town, 100).size() == 33);
    std::puts("word_count_test: OK");
    return 0;
}
