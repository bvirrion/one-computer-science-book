// pc_cpp.cpp: two producers, two consumers, a queue of 8.
#include <cstdio>
#include <thread>
#include <vector>

#include "bounded_queue.hpp"

int main()
{
    constexpr long items = 100'000;
    BoundedQueue<long, 8> q;
    long sums[2] = {0, 0};
    {
        std::vector<std::jthread> team;              // joined at the end of the block
        for (int i = 0; i < 2; i++) {
            team.emplace_back([&q] {
                for (long k = 1; k <= items; k++)
                    q.put(k);
            });
            team.emplace_back([&q, &s = sums[i]] {
                for (long k = 0; k < items; k++)
                    s += q.take();
            });
        }
    }
    std::printf("sum taken: %ld, sum put: %ld\n", sums[0] + sums[1], items * (items + 1));
}
