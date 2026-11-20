// txn_file.hpp: exercise 10, a file that appears whole on commit or not at all.
#pragma once
#include <cstdio>
#include <stdexcept>
#include <string>
#include <utility>

class TxnFile {
public:
    explicit TxnFile(std::string path)
        : path_(std::move(path)), tmp_(path_ + ".tmp"), f_(std::fopen(tmp_.c_str(), "w"))
    {
        if (f_ == nullptr)
            throw std::runtime_error("cannot create " + tmp_);
    }
    ~TxnFile()
    {
        if (f_ != nullptr)
            std::fclose(f_);
        if (!committed_)
            std::remove(tmp_.c_str());     // unwinding or no commit: nothing appears
    }
    TxnFile(const TxnFile &) = delete;
    TxnFile &operator=(const TxnFile &) = delete;

    void write(const std::string &s)
    {
        if (std::fputs(s.c_str(), f_) == EOF)
            throw std::runtime_error("write failed");
    }
    void commit()
    {
        int closed = std::fclose(f_);
        f_ = nullptr;
        if (closed != 0 || std::rename(tmp_.c_str(), path_.c_str()) != 0)
            throw std::runtime_error("commit failed");
        committed_ = true;
    }

private:
    std::string path_, tmp_;
    std::FILE *f_;
    bool committed_ = false;
};
