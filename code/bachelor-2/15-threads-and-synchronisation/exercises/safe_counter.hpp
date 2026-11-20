// safe_counter.hpp: a counter that many threads may use at once (exercise 3).
#ifndef SAFE_COUNTER_HPP
#define SAFE_COUNTER_HPP

#include <mutex>

class SafeCounter {
public:
    void add(long d)
    {
        std::lock_guard<std::mutex> g(m_);       // unlocked by g's destructor
        value_ += d;
    }

    bool take(long d)                            // subtract d if the counter holds d
    {
        std::lock_guard<std::mutex> g(m_);
        if (value_ < d)
            return false;                        // early return: still unlocked
        value_ -= d;
        return true;
    }

    long get() const
    {
        std::lock_guard<std::mutex> g(m_);
        return value_;
    }

private:
    mutable std::mutex m_;                       // get() is const, yet locks
    long value_ = 0;
};

#endif
