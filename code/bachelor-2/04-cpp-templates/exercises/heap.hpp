// heap.hpp (exercise 10): a binary heap of T; the comparator is a template parameter.
#pragma once
#include <cstddef>
#include <functional>
#include <stdexcept>
#include <utility>
#include <vector>

// With Less = std::less<T>, top() is the largest element (Less says which is "smaller").
template <typename T, typename Less = std::less<T>>
class Heap {
public:
    explicit Heap(Less less = Less()) : less_(less) {}
    void push(T x)
    {
        v_.push_back(std::move(x));
        std::size_t i = v_.size() - 1;
        while (i > 0 && less_(v_[(i - 1) / 2], v_[i])) {     // sift up
            std::swap(v_[(i - 1) / 2], v_[i]);
            i = (i - 1) / 2;
        }
    }
    const T &top() const
    {
        if (v_.empty()) throw std::out_of_range("Heap::top on an empty heap");
        return v_[0];
    }
    void pop()
    {
        if (v_.empty()) throw std::out_of_range("Heap::pop on an empty heap");
        v_[0] = std::move(v_.back());
        v_.pop_back();
        std::size_t i = 0, n = v_.size();
        for (;;) {                                              // sift down
            std::size_t l = 2 * i + 1, r = l + 1, m = i;
            if (l < n && less_(v_[m], v_[l])) m = l;
            if (r < n && less_(v_[m], v_[r])) m = r;
            if (m == i) break;
            std::swap(v_[i], v_[m]);
            i = m;
        }
    }
    std::size_t size() const { return v_.size(); }
    bool empty() const { return v_.empty(); }

private:
    std::vector<T> v_;
    Less less_;
};
