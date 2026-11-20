// interval_map.hpp: a value for every int key, stored as the points where it changes (exercise 10).
#pragma once
#include <iterator>
#include <map>
#include <utility>

template <typename V>
class IntervalMap {
public:
    explicit IntervalMap(V initial) : initial_(std::move(initial)) {}

    const V &operator[](int key) const            // O(log n): the last change at or before key
    {
        auto it = changes_.upper_bound(key);
        return it == changes_.begin() ? initial_ : std::prev(it)->second;
    }

    void assign(int lo, int hi, const V &v)         // the keys lo <= k < hi get v
    {
        if (!(lo < hi))
            return;
        V after = (*this)[hi];                      // the value that resumes at hi
        auto first = changes_.lower_bound(lo), last = changes_.lower_bound(hi);
        bool has_hi = last != changes_.end() && last->first == hi;
        changes_.erase(first, last);                // the old changes inside [lo, hi)
        changes_[lo] = v;
        if (!has_hi)
            changes_[hi] = after;
        canonical(lo);
        canonical(hi);
    }

    std::size_t changes() const { return changes_.size(); }

private:
    void canonical(int key)                   // drop a change that repeats the value before it
    {
        auto it = changes_.find(key);
        if (it == changes_.end())
            return;
        const V &before = it == changes_.begin() ? initial_ : std::prev(it)->second;
        if (it->second == before)
            changes_.erase(it);
    }

    V initial_;
    std::map<int, V> changes_;                      // key -> value from this key on
};
