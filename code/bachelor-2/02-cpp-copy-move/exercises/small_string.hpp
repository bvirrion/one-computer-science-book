// small_string.hpp (exercise 10): short strings inside the object, long ones on the heap.
#pragma once
#include <cstddef>
#include <cstring>
#include <utility>

class SmallString {
public:
    static constexpr std::size_t inline_cap = 15;      // characters kept without the heap

    SmallString(const char *s = "") { init(s, std::strlen(s)); }
    ~SmallString() { if (!is_small()) delete[] ptr_; }
    SmallString(const SmallString &o) { init(o.ptr_, o.n_); }
    SmallString(SmallString &&o) noexcept : n_(o.n_)
    {
        if (o.is_small()) {
            std::memcpy(buf_, o.buf_, n_ + 1);         // nothing to steal: copy the few bytes
            ptr_ = buf_;
        } else {
            ptr_ = std::exchange(o.ptr_, o.buf_);      // steal the block
        }
        o.n_ = 0;
        o.buf_[0] = '\0';
    }
    SmallString &operator=(const SmallString &o)
    {
        if (this != &o) {
            SmallString tmp(o);                        // may throw; *this untouched
            *this = std::move(tmp);
        }
        return *this;
    }
    SmallString &operator=(SmallString &&o) noexcept
    {
        if (this != &o) {
            this->~SmallString();
            new (this) SmallString(std::move(o));      // reuse the move constructor
        }
        return *this;
    }
    const char *c_str() const { return ptr_; }
    std::size_t size() const { return n_; }
    bool is_small() const { return ptr_ == buf_; }

private:
    void init(const char *s, std::size_t n)
    {
        n_ = n;
        ptr_ = n <= inline_cap ? buf_ : new char[n + 1];
        std::memcpy(ptr_, s, n);
        ptr_[n] = '\0';
    }
    std::size_t n_ = 0;
    char *ptr_ = buf_;
    char buf_[inline_cap + 1] = {};
};
