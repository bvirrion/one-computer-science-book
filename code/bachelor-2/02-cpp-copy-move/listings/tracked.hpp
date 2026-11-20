// tracked.hpp: values that count how often they are copied and moved.
#pragma once

struct Counts {
    long copies = 0, moves = 0;
};
inline Counts counts;                  // one counter for the whole program

class Tracked {                        // its move constructor promises not to throw
public:
    explicit Tracked(int v = 0) : v_(v) {}
    Tracked(const Tracked &o) : v_(o.v_) { counts.copies++; }
    Tracked(Tracked &&o) noexcept : v_(o.v_) { counts.moves++; }
    Tracked &operator=(const Tracked &o) { v_ = o.v_; counts.copies++; return *this; }
    Tracked &operator=(Tracked &&o) noexcept { v_ = o.v_; counts.moves++; return *this; }
    int value() const { return v_; }

private:
    int v_;
};

class TrackedMayThrow {                // the same, without noexcept on the moves
public:
    explicit TrackedMayThrow(int v = 0) : v_(v) {}
    TrackedMayThrow(const TrackedMayThrow &o) : v_(o.v_) { counts.copies++; }
    TrackedMayThrow(TrackedMayThrow &&o) : v_(o.v_) { counts.moves++; }
    TrackedMayThrow &operator=(const TrackedMayThrow &o)
        { v_ = o.v_; counts.copies++; return *this; }
    TrackedMayThrow &operator=(TrackedMayThrow &&o)
        { v_ = o.v_; counts.moves++; return *this; }
    int value() const { return v_; }

private:
    int v_;
};
