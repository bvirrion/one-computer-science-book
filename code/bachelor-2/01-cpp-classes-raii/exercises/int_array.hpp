// int_array.hpp: exercise 3, a fixed-size array of ints that owns its heap block.
#pragma once
#include <cstddef>
#include <stdexcept>
#include <string>

class IntArray {
public:
    explicit IntArray(std::size_t n) : n_(n), data_(new int[n]{}) {}   // zero-filled
    ~IntArray() { delete[] data_; }
    IntArray(const IntArray &) = delete;
    IntArray &operator=(const IntArray &) = delete;

    std::size_t size() const { return n_; }
    int &at(std::size_t i) { return data_[check(i)]; }
    const int &at(std::size_t i) const { return data_[check(i)]; }

private:
    std::size_t check(std::size_t i) const
    {
        if (i >= n_)
            throw std::out_of_range("IntArray index " + std::to_string(i));
        return i;
    }
    std::size_t n_;
    int *data_;
};
