// matrix.hpp (exercise 9): matrices whose dimensions are part of their type.
#pragma once
#include <array>
#include <cstddef>

template <typename T, std::size_t R, std::size_t C>
struct Matrix {
    std::array<T, R * C> a{};               // row by row
    T &operator()(std::size_t i, std::size_t j) { return a[i * C + j]; }
    const T &operator()(std::size_t i, std::size_t j) const { return a[i * C + j]; }
};

// (R x K) times (K x C): the shared K is checked by the compiler, not at run time.
template <typename T, std::size_t R, std::size_t K, std::size_t C>
Matrix<T, R, C> operator*(const Matrix<T, R, K> &x, const Matrix<T, K, C> &y)
{
    Matrix<T, R, C> z;
    for (std::size_t i = 0; i < R; i++)
        for (std::size_t j = 0; j < C; j++)
            for (std::size_t k = 0; k < K; k++)
                z(i, j) += x(i, k) * y(k, j);
    return z;
}

template <typename T, std::size_t R, std::size_t C>
Matrix<T, C, R> transpose(const Matrix<T, R, C> &x)
{
    Matrix<T, C, R> t;
    for (std::size_t i = 0; i < R; i++)
        for (std::size_t j = 0; j < C; j++)
            t(j, i) = x(i, j);
    return t;
}
