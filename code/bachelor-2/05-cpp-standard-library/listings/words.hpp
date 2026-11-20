// words.hpp: count the words of the titles in a CSV of books (title in the second column).
#pragma once
#include <algorithm>
#include <cctype>
#include <istream>
#include <map>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

inline std::string title_of(const std::string &line)   // the second comma-separated field
{
    std::size_t a = line.find(','), b = line.find(',', a + 1);
    return line.substr(a + 1, b - a - 1);
}

inline std::map<std::string, int> count_words(std::istream &in)
{
    std::map<std::string, int> count;                   // a balanced search tree: kept sorted
    std::string line, word;
    std::getline(in, line);                             // skip the header
    while (std::getline(in, line)) {
        std::istringstream title(title_of(line));
        while (title >> word) {
            std::transform(word.begin(), word.end(), word.begin(),
                [](unsigned char c) { return std::tolower(c); });
            count[word]++;                              // a missing key starts at 0
        }
    }
    return count;
}

inline std::vector<std::pair<std::string, int>> by_frequency(const std::map<std::string, int> &count)
{
    std::vector<std::pair<std::string, int>> v(count.begin(), count.end());
    std::stable_sort(v.begin(), v.end(), [](const auto &a, const auto &b) { return a.second > b.second; });
    return v;                                           // ties stay in alphabetical order
}
