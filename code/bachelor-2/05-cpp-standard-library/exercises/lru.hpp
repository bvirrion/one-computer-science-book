// lru.hpp: a least-recently-used cache of fixed capacity, a list plus a hash map (exercise 9).
#pragma once
#include <cstddef>
#include <list>
#include <optional>
#include <unordered_map>
#include <utility>

template <typename K, typename V>
class LruCache {
public:
    explicit LruCache(std::size_t capacity) : cap_(capacity) {}

    std::optional<V> get(const K &key)              // O(1) on average; makes the key the most recent
    {
        auto it = where_.find(key);
        if (it == where_.end())
            return std::nullopt;
        order_.splice(order_.begin(), order_, it->second);   // move the node to the front, no copy
        return it->second->second;
    }

    void put(const K &key, V value)                 // O(1) on average; evicts the least recent if full
    {
        if (auto it = where_.find(key); it != where_.end()) {
            it->second->second = std::move(value);
            order_.splice(order_.begin(), order_, it->second);
            return;
        }
        if (order_.size() == cap_) {
            where_.erase(order_.back().first);
            order_.pop_back();
        }
        order_.emplace_front(key, std::move(value));
        where_[key] = order_.begin();               // list iterators stay valid when others are erased
    }

    std::size_t size() const { return order_.size(); }

private:
    std::size_t cap_;
    std::list<std::pair<K, V>> order_;              // most recent first
    std::unordered_map<K, typename std::list<std::pair<K, V>>::iterator> where_;
};
