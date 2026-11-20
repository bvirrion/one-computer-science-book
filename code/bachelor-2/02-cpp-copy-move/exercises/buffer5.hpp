// buffer5.hpp (exercise 3): Buffer with the rule of five.
#pragma once
#include <cstddef>
#include <cstring>
#include <utility>

class Buffer {
public:
    explicit Buffer(const char *text) : n_(std::strlen(text)), data_(new char[n_ + 1])
    {
        std::memcpy(data_, text, n_ + 1);
    }
    ~Buffer() { delete[] data_; }
    Buffer(const Buffer &o) : n_(o.n_), data_(new char[o.n_ + 1])
    {
        std::memcpy(data_, o.data_, n_ + 1);
    }
    Buffer(Buffer &&o) noexcept : n_(std::exchange(o.n_, 0)),
        data_(std::exchange(o.data_, nullptr)) {}
    Buffer &operator=(Buffer o) noexcept  // by value: copied or moved by the caller's argument
    {
        std::swap(n_, o.n_);
        std::swap(data_, o.data_);
        return *this;                         // o dies with the old block
    }
    const char *c_str() const { return data_ ? data_ : ""; }
    std::size_t size() const { return n_; }

private:
    std::size_t n_;
    char *data_;
};
