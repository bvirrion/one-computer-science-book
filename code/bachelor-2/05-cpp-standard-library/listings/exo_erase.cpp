// exo_erase.cpp: remove the even values. The output is wrong.
#include <cstdio>
#include <vector>

int main()
{
    std::vector<int> v{3, 8, 12, 5, 6, 6, 7, 10};
    for (std::size_t i = 0; i < v.size(); i++)
        if (v[i] % 2 == 0)
            v.erase(v.begin() + long(i));
    for (int x : v)
        std::printf("%d ", x);
    std::printf("\n");
    return 0;
}
