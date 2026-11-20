// workload.hpp: one stream of reservations served by three containers (exercise 12).
#pragma once
#include <algorithm>
#include <functional>
#include <queue>
#include <set>
#include <vector>

// ops: a value >= 0 adds that waiting member's number; -1 serves (pops) the smallest
struct HeapQueue {
    std::priority_queue<int, std::vector<int>, std::greater<int>> q;
    void add(int x) { q.push(x); }
    int serve() { int x = q.top(); q.pop(); return x; }
    bool empty() const { return q.empty(); }
};
struct SetQueue {
    std::multiset<int> s;                           // a balanced tree: duplicates allowed
    void add(int x) { s.insert(x); }
    int serve() { int x = *s.begin(); s.erase(s.begin()); return x; }
    bool empty() const { return s.empty(); }
};
struct SortedVectorQueue {
    std::vector<int> v;                // kept in decreasing order: the smallest is at the back
    void add(int x) {
        v.insert(std::lower_bound(v.begin(), v.end(), x, std::greater<int>()), x); }
    int serve() { int x = v.back(); v.pop_back(); return x; }
    bool empty() const { return v.empty(); }
};

template <class Q> std::vector<int> run(const std::vector<int> &ops)  // the values served
{
    Q q;
    std::vector<int> served;
    for (int op : ops)
        if (op >= 0)
            q.add(op);
        else if (!q.empty())
            served.push_back(q.serve());
    return served;
}
