// binomial.hpp (exercise 12): Pascal's triangle computed by the compiler.
#pragma once
#include <array>
#include <cstdint>

template <std::size_t N>
constexpr std::array<std::array<std::uint64_t, N + 1>, N + 1> pascal()
{
    std::array<std::array<std::uint64_t, N + 1>, N + 1> c{};
    for (std::size_t n = 0; n <= N; n++) {
        c[n][0] = 1;
        for (std::size_t k = 1; k <= n; k++)
            c[n][k] = c[n - 1][k - 1] + c[n - 1][k];    // c[n-1][n] is 0
    }
    return c;
}

inline constexpr auto BINOM = pascal<67>();           // the last full row that fits in 64 bits

static_assert(BINOM[5][2] == 10);
static_assert(BINOM[67][33] == 14226520737620288370ULL);
