// exo_observers.cpp (exercise 12): stations and the displays that watch them.
// capture: cflags=-O0 -g -fsanitize=address exit
#include <cstdio>
#include <memory>
#include <string>
#include <vector>

struct Display;
struct Station {
    std::string name;
    std::vector<std::shared_ptr<Display>> watchers;     // to notify on each reading
    ~Station() { std::printf("free station %s\n", name.c_str()); }
};
struct Display {
    std::string room;
    std::shared_ptr<Station> source;                   // the station shown
    ~Display() { std::printf("free display %s\n", room.c_str()); }
};

void watch(const std::shared_ptr<Station> &s, const std::string &room)
{
    auto d = std::make_shared<Display>();
    d->room = room;
    d->source = s;
    s->watchers.push_back(d);
}

int main()
{
    auto s = std::make_shared<Station>();
    s->name = "Riverside";
    watch(s, "hall");
    watch(s, "office");
    std::printf("station count %ld\n", s.use_count());
    std::fflush(stdout);
    return 0;
}
