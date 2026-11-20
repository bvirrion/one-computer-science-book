// weak_fix.cpp: the photo observes its album instead of owning it.
// capture: cflags=-O0 -g -fsanitize=address
#include <cstdio>
#include <memory>
#include <string>

struct Album;
struct Photo {
    std::string name;
    std::weak_ptr<Album> album;                 // does not keep the album alive
    ~Photo() { std::printf("free photo %s\n", name.c_str()); }
};
struct Album {
    std::string title;
    std::shared_ptr<Photo> cover;
    ~Album() { std::printf("free album %s\n", title.c_str()); }
};

int main()
{
    auto p = std::make_shared<Photo>();
    p->name = "pier.jpg";
    {
        auto a = std::make_shared<Album>();
        a->title = "Coast";
        p->album = a;
        a->cover = p;
        if (auto alb = p->album.lock())         // a shared_ptr while we use it
            std::printf("pier.jpg is in %s (album count %ld)\n",
                alb->title.c_str(), a.use_count());
    }
    std::printf("album gone: %s\n", p->album.expired() ? "yes" : "no");
    return 0;
}
