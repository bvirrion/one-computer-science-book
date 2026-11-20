// scope_guard.hpp: exercise 7, run an action when the scope ends, unless dismissed.
#pragma once
#include <utility>

template <class F> class ScopeGuard {
public:
    explicit ScopeGuard(F action) : action_(std::move(action)) {}
    ~ScopeGuard()
    {
        if (active_)
            action_();
    }
    void dismiss() noexcept { active_ = false; }
    ScopeGuard(const ScopeGuard &) = delete;
    ScopeGuard &operator=(const ScopeGuard &) = delete;

private:
    F action_;
    bool active_ = true;
};
