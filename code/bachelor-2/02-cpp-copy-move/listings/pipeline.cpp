// pipeline.cpp: an editing pipeline over images held by value.
#include <cstdio>
#include <cstdint>
#include <utility>
#include <vector>

long copies = 0, moves = 0;

class Image {
public:
    Image(int w, int h) : w_(w), h_(h), px_(std::size_t(w) * h, 128) {}
    Image(const Image &o) : w_(o.w_), h_(o.h_), px_(o.px_) { copies++; }
    Image(Image &&o) noexcept : w_(o.w_), h_(o.h_), px_(std::move(o.px_)) { moves++; }
    Image &operator=(const Image &o) { w_ = o.w_; h_ = o.h_; px_ = o.px_; copies++; return *this; }
    Image &operator=(Image &&o) noexcept { w_ = o.w_; h_ = o.h_; px_ = std::move(o.px_); moves++; return *this; }
    void add(int d) { for (auto &p : px_) p = std::uint8_t(p + d); }
    std::size_t bytes() const { return px_.size(); }

private:
    int w_, h_;
    std::vector<std::uint8_t> px_;
};

// Version 1: parameters by const reference, results by value.
Image brighten1(const Image &im) { Image out = im; out.add(10); return out; }
Image darken1(const Image &im) { Image out = im; out.add(-5); return out; }
// Version 2: parameters by value, changed in place and returned.
Image brighten2(Image im) { im.add(10); return im; }
Image darken2(Image im) { im.add(-5); return im; }

void report(const char *what)
{
    std::printf("%-34s %ld copies, %ld moves\n", what, copies, moves);
    copies = moves = 0;
}

int main()
{
    Image photo(4000, 3000);
    Image a = darken1(brighten1(photo));            report("1: const& in, value out");
    Image b = darken2(brighten2(photo));            report("2: by value, photo kept");
    Image c = darken2(brighten2(std::move(photo))); report("2: by value, photo moved in");
    std::vector<Image> album;
    album.push_back(a);
    album.push_back(std::move(b));
    album.push_back(std::move(c));                  report("3: three pushes, no reserve");
    std::printf("each copy: %zu bytes\n", a.bytes());
    return 0;
}
