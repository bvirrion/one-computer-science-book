// constexpr_pow.cpp: a function the compiler can run while it compiles.
#include <cstdint>
#include <cstdio>

constexpr std::uint64_t power(std::uint64_t b, unsigned e)
{
    std::uint64_t r = 1;
    while (e--)
        r *= b;
    return r;
}

static_assert(power(2, 10) == 1024);            // checked at compile time
constexpr std::uint64_t KIB = power(2, 10), GIB = power(KIB, 3);
int table[power(3, 4)];                          // an array size must be a constant: 81

int main(int argc, char **)
{
    std::printf("%llu %llu %zu\n", (unsigned long long)GIB,
        (unsigned long long)power(argc + 1, 20),
                sizeof table / sizeof table[0]);
    return 0;
}
