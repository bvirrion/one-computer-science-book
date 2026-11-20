// buckets.cpp: eight street names in a std::map (a search tree) and a std::unordered_map (a hash table).
#include <cstdio>
#include <map>
#include <string>
#include <unordered_map>

int main()
{
    const char *names[] = {"Mill Row", "Bridge Road", "Station Row", "Castle Way",
                           "River Lane", "Garden Lane", "Orchard Way", "Church Lane"};
    std::map<std::string, int> tree;
    std::unordered_map<std::string, int> table;
    for (int i = 0; i < 8; i++) {
        tree[names[i]] = i + 1;                     // the street's number in the list
        table[names[i]] = i + 1;
    }
    int k = 0;
    for (const auto &[name, n] : tree)              // in increasing order of the key
        std::printf("%s%s(%d)", k++ % 4 ? " " : k > 1 ? "\n     " : "map: ", name.c_str(), n);
    k = 0;
    for (const auto &[name, n] : table)             // in an order set by the hashes
        std::printf("%s%s(%d)", k++ % 4 ? " " : k > 1 ? "\n     " : "\nunordered_map:\n     ",
            name.c_str(), n);
    std::printf("\n%zu elements, %zu buckets, load factor %.2f, max %.1f\n", table.size(),
                table.bucket_count(), table.load_factor(), table.max_load_factor());
    for (std::size_t b = 0; b < table.bucket_count(); b++) {
        std::printf("bucket %2zu:", b);
        for (auto it = table.begin(b); it != table.end(b); ++it)
            std::printf(" %s", it->first.c_str());
        std::printf("\n");
    }
    return 0;
}
