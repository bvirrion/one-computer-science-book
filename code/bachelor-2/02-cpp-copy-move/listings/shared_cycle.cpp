// shared_cycle.cpp: two shared owners of each other are never freed.
// capture: cflags=-O0 -g -fsanitize=address exit
#include <cstdio>
#include <memory>
#include <string>

struct Album;
struct Photo {
    std::string name;
    std::shared_ptr<Album> album;               // a photo keeps its album alive
    ~Photo() { std::printf("free photo %s\n", name.c_str()); }
};
struct Album {
    std::string title;
    std::shared_ptr<Photo> cover;               // an album keeps its cover alive
    ~Album() { std::printf("free album %s\n", title.c_str()); }
};

int main()
{
    auto a = std::make_shared<Album>();
    a->title = "Coast";
    auto p = std::make_shared<Photo>();
    p->name = "pier.jpg";
    p->album = a;
    a->cover = p;
    std::printf("counts: album %ld, photo %ld\n", a.use_count(), p.use_count());
    std::fflush(stdout);                        // the leak report ends the program at once
    return 0;                                   // a and p die; the counts drop to 1
}
