// unique_ptr.hpp (exercise 7): a minimal move-only owner of one heap object.
#pragma once
#include <utility>

template <class T> class UniquePtr {
public:
    UniquePtr() noexcept = default;
    explicit UniquePtr(T *p) noexcept : p_(p) {}
    ~UniquePtr() { delete p_; }
    UniquePtr(const UniquePtr &) = delete;
    UniquePtr &operator=(const UniquePtr &) = delete;
    UniquePtr(UniquePtr &&o) noexcept : p_(std::exchange(o.p_, nullptr)) {}
    UniquePtr &operator=(UniquePtr &&o) noexcept
    {
        if (this != &o)
            reset(std::exchange(o.p_, nullptr));
        return *this;
    }
    T &operator*() const { return *p_; }
    T *operator->() const noexcept { return p_; }
    T *get() const noexcept { return p_; }
    explicit operator bool() const noexcept { return p_ != nullptr; }
    T *release() noexcept { return std::exchange(p_, nullptr); }
    void reset(T *p = nullptr) noexcept
    {
        T *old = std::exchange(p_, p);        // set first: old's destructor may look at us
        delete old;
    }

private:
    T *p_ = nullptr;
};
