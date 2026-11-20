// bounded_stack.hpp: exercise 9, a stack of at most N elements; push is strong.
#pragma once
#include <cstddef>
#include <stdexcept>
#include <vector>

template <class T, std::size_t N> class BoundedStack {
public:
    BoundedStack() { items_.reserve(N); }   // after this, push_back never reallocates

    // Strong guarantee: if push throws (full stack, or T's copy throws), *this is unchanged.
    void push(const T &x)
    {
        if (items_.size() == N)
            throw std::length_error("stack full");
        items_.push_back(x);   // no reallocation: a throwing copy leaves items_ as it was
    }
    void pop()
    {
        if (items_.empty())
            throw std::out_of_range("stack empty");
        items_.pop_back();
    }
    const T &top() const
    {
        if (items_.empty())
            throw std::out_of_range("stack empty");
        return items_.back();
    }
    std::size_t size() const { return items_.size(); }

private:
    std::vector<T> items_;
};
