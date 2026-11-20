// pc_test.cpp: BoundedQueue keeps order and loses nothing; SafeCounter under 8 threads.
#include <cassert>
#include <cstdio>
#include <thread>
#include <vector>

#include "../exercises/safe_counter.hpp"
#include "bounded_queue.hpp"

int main()
{
    {
        BoundedQueue<int, 4> q;                  // one producer, one consumer: FIFO
        std::vector<int> got;
        {
            std::jthread p([&] { for (int k = 0; k < 10000; k++) q.put(k); });
            std::jthread c([&] { for (int k = 0; k < 10000; k++) got.push_back(q.take()); });
        }
        for (int k = 0; k < 10000; k++)
            assert(got[k] == k);
    }
    {
        BoundedQueue<long, 3> q;                 // 4 producers, 4 consumers
        std::vector<long> sums(4, 0);
        {
            std::vector<std::jthread> team;
            for (int i = 0; i < 4; i++) {
                team.emplace_back([&] { for (long k = 1; k <= 20000; k++) q.put(k); });
                team.emplace_back([&, i] { for (int k = 0; k < 20000; k++) sums[i] += q.take(); });
            }
        }
        assert(sums[0] + sums[1] + sums[2] + sums[3] == 4L * 20000 * 20001 / 2);
    }
    {
        SafeCounter c;
        {
            std::vector<std::jthread> team;
            for (int i = 0; i < 8; i++)
                team.emplace_back([&] {
                    for (int k = 0; k < 10000; k++) {
                        c.add(2);
                        while (!c.take(1)) {
                        }
                    }
                });
        }
        assert(c.get() == 80000);
        assert(!c.take(80001) && c.take(80000) && c.get() == 0);
    }
    std::printf("pc_test: all passed\n");
}
