// counter_threads.cpp: the counter of race.c with std::thread, std::mutex and std::atomic.
#include <atomic>
#include <cstdio>
#include <mutex>
#include <thread>
#include <vector>

int main()
{
    constexpr long n = 1'000'000;
    long plain = 0;
    std::mutex m;
    std::atomic<long> atom{0};
    std::vector<std::thread> threads;
    for (int i = 0; i < 4; i++)
        threads.emplace_back([&] {                    // captures by reference: shared
            for (long k = 0; k < n; k++) {
                {
                    std::lock_guard<std::mutex> guard(m);   // locks here ...
                    plain++;
                }                                           // ... unlocks here, always
                atom.fetch_add(1);
            }
        });
    for (auto &t : threads)
        t.join();
    std::printf("mutex: %ld, atomic: %ld, expected %ld\n", plain, atom.load(), 4 * n);
}
