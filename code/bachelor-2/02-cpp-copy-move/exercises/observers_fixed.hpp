// observers_fixed.hpp (exercise 12): displays observe their station; the station owns them.
#pragma once
#include <memory>
#include <string>
#include <vector>

inline int alive = 0;                                  // objects not yet destroyed

struct Display;
struct Station {
    std::string name;
    std::vector<std::shared_ptr<Display>> watchers;    // owns its displays
    Station() { alive++; }
    ~Station() { alive--; }
};
struct Display {
    std::string room;
    std::weak_ptr<Station> source;                     // observes: the fix
    Display() { alive++; }
    ~Display() { alive--; }
};

inline void watch(const std::shared_ptr<Station> &s, const std::string &room)
{
    auto d = std::make_shared<Display>();
    d->room = room;
    d->source = s;
    s->watchers.push_back(d);
}
