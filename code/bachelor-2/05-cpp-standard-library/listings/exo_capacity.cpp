// exo_capacity.cpp: when does push_back move the elements of a vector?
#include <cstdio>
#include <vector>

int main()
{
    std::vector<int> v;
    const int *block = v.data();
    for (int i = 1; i <= 1000; i++) {
        v.push_back(i);
        if (v.data() != block) {                      // a new block: every iterator is invalid
            std::printf("%d:%zu ", i, v.capacity());
            block = v.data();
        }
    }
    std::printf("\n");
    return 0;
}
