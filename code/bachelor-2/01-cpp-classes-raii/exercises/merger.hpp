// merger.hpp: exercise 6 fixed; each file is a member that owns itself.
#pragma once
#include "file_handle.hpp"

class Merger {
public:
    Merger(const char *first, const char *second) : a_(first, "r"), b_(second, "r") {}
    // No destructor to write: a_ and b_ close themselves. If b_'s constructor throws,
    // the fully built member a_ is destroyed before the exception leaves.

private:
    File a_;
    File b_;
};
