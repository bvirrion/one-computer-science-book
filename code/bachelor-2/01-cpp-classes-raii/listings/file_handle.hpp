// file_handle.hpp: a FILE* owned by an object; the destructor closes it.
#pragma once
#include <cstdio>
#include <optional>
#include <stdexcept>
#include <string>

class File {
public:
    File(const std::string &path, const char *mode) : f_(std::fopen(path.c_str(), mode))
    {
        if (f_ == nullptr)
            throw std::runtime_error("cannot open " + path);
    }
    ~File() { std::fclose(f_); }
    File(const File &) = delete;             // one owner: no copies
    File &operator=(const File &) = delete;

    std::optional<std::string> read_line()   // without its newline; nothing at the end
    {
        std::string line;
        int c;
        while ((c = std::fgetc(f_)) != EOF && c != '\n')
            line += static_cast<char>(c);
        if (c == EOF && line.empty())
            return std::nullopt;
        return line;
    }
    void write(const std::string &s)
    {
        if (std::fputs(s.c_str(), f_) == EOF)
            throw std::runtime_error("write failed");
    }
    void flush()                             // a full disk shows up here, not in write
    {
        if (std::fflush(f_) == EOF)
            throw std::runtime_error("flush failed");
    }

private:
    std::FILE *f_;
};
