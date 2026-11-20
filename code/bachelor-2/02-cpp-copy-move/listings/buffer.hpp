// buffer.hpp: a buffer with a deep copy (rule of three).
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
    Buffer(const Buffer &o) : n_(o.n_), data_(new char[o.n_ + 1])   // a block of its own
    {
        std::memcpy(data_, o.data_, n_ + 1);
    }
    Buffer &operator=(const Buffer &o)          // copy and swap
    {
        Buffer tmp(o);                          // may throw: *this not touched yet
        std::swap(n_, tmp.n_);
        std::swap(data_, tmp.data_);
        return *this;                           // tmp dies with the old block
    }
    const char *c_str() const { return data_; }
    std::size_t size() const { return n_; }
    void upcase_first() { if (n_ > 0 && data_[0] >= 'a' && data_[0] <= 'z') data_[0] -= 32; }

private:
    std::size_t n_;
    char *data_;
};
