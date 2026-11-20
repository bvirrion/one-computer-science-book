// vec.hpp: a growable array of any type T, with the rule of five.
#pragma once
#include <cstddef>
#include <new>
#include <stdexcept>
#include <utility>

template <typename T>
class Vec {
public:
    Vec() = default;
    ~Vec() { clear(); ::operator delete(data_); }
    Vec(const Vec &o) : Vec()
    {
        reserve(o.size_);
        for (std::size_t i = 0; i < o.size_; i++)
            push_back(o[i]);
    }
    Vec(Vec &&o) noexcept
        : data_(std::exchange(o.data_, nullptr)), size_(std::exchange(o.size_, 0)),
          cap_(std::exchange(o.cap_, 0)) {}
    Vec &operator=(Vec o) noexcept      // copy and swap; moves when given an rvalue
    {
        std::swap(data_, o.data_);
        std::swap(size_, o.size_);
        std::swap(cap_, o.cap_);
        return *this;
    }

    void push_back(T x)                 // x is a copy or a moved value; it is moved in
    {
        if (size_ == cap_)
            reserve(cap_ ? 2 * cap_ : 1);
        new (data_ + size_) T(std::move(x));    // construct in raw memory
        size_++;
    }
    void reserve(std::size_t n)
    {
        if (n <= cap_)
            return;
        T *p = static_cast<T *>(::operator new(n * sizeof(T)));   // raw memory, no T built
        std::size_t i = 0;
        try {
            for (; i < size_; i++)                  // moves if they cannot throw, else copies
                new (p + i) T(std::move_if_noexcept(data_[i]));
        } catch (...) {                          // a copy threw: undo, the old block is intact
            while (i > 0)
                p[--i].~T();
            ::operator delete(p);
            throw;
        }
        clear();
        ::operator delete(data_);
        data_ = p;
        size_ = i;
        cap_ = n;
    }
    void clear() noexcept
    {
        for (std::size_t i = size_; i > 0; i--)
            data_[i - 1].~T();          // destroy in reverse order
        size_ = 0;
    }
    T &operator[](std::size_t i) { return data_[i]; }
    const T &operator[](std::size_t i) const { return data_[i]; }
    T &at(std::size_t i) { if (i >= size_) throw std::out_of_range("Vec::at"); return data_[i]; }
    std::size_t size() const { return size_; }
    std::size_t capacity() const { return cap_; }
    T *begin() { return data_; }
    T *end() { return data_ + size_; }

private:
    T *data_ = nullptr;
    std::size_t size_ = 0, cap_ = 0;
};
