// unique.cpp: one owner at a time; the owner frees.
// capture: cflags=-O0 -g -fsanitize=address
#include <cstdio>
#include <memory>
#include <string>
#include <vector>

struct Photo {
    std::string name;
    explicit Photo(std::string n) : name(std::move(n))
        { std::printf("  load %s\n", name.c_str()); }
    ~Photo() { std::printf("  free %s\n", name.c_str()); }
};

std::unique_ptr<Photo> open_photo(const char *name)
{
    return std::make_unique<Photo>(name);        // ownership leaves the function
}

int main()
{
    std::vector<std::unique_ptr<Photo>> album;
    album.push_back(open_photo("pier.jpg"));
    auto p = open_photo("dunes.jpg");
    album.push_back(std::move(p));               // album.push_back(p) does not compile
    std::printf("p is %s, album holds %zu\n", p ? "full" : "empty", album.size());
    album.erase(album.begin());                  // the photo goes with its owner
    std::puts("end of main");
    return 0;
}
