// bounded_queue.hpp: a ring of N slots guarded by two counting semaphores and a mutex.
#ifndef BOUNDED_QUEUE_HPP
#define BOUNDED_QUEUE_HPP

#include <array>
#include <cstddef>
#include <mutex>
#include <semaphore>

template <typename T, std::ptrdiff_t N>
class BoundedQueue {
public:
    void put(T x)
    {
        free_.acquire();                         // a free slot, or wait
        {
            std::lock_guard<std::mutex> g(m_);
            ring_[in_] = std::move(x);
            in_ = (in_ + 1) % N;
        }
        filled_.release();
    }

    T take()
    {
        filled_.acquire();                       // a filled slot, or wait
        T x;
        {
            std::lock_guard<std::mutex> g(m_);
            x = std::move(ring_[out_]);
            out_ = (out_ + 1) % N;
        }
        free_.release();
        return x;
    }

private:
    std::array<T, N> ring_{};
    std::ptrdiff_t in_ = 0, out_ = 0;
    std::mutex m_;
    std::counting_semaphore<N> free_{N}, filled_{0};
};

#endif
