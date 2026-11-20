// exo_selfassign.cpp (exercise 2): an assignment written the obvious way.
#include <cstdio>
#include <cstring>

class Text {
public:
    explicit Text(const char *s) : data_(new char[std::strlen(s) + 1])
        { std::strcpy(data_, s); }
    ~Text() { delete[] data_; }
    Text(const Text &o) : data_(new char[std::strlen(o.data_) + 1])
        { std::strcpy(data_, o.data_); }
    Text &operator=(const Text &o)
    {
        delete[] data_;                                  // free the old text
        data_ = new char[std::strlen(o.data_) + 1];      // take room for the new one
        std::strcpy(data_, o.data_);
        return *this;
    }
    const char *c_str() const { return data_; }

private:
    char *data_;
};

int main()
{
    Text t("Old Harbour");
    Text &alias = t;
    t = alias;
    std::puts(t.c_str());
    return 0;
}
