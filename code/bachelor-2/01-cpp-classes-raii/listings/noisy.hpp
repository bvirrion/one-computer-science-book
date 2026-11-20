// noisy.hpp: an object that prints when it is made and when it is destroyed.
#pragma once
#include <iostream>
#include <string>

class Noisy {
public:
    explicit Noisy(std::string name) : name_(std::move(name))
    {
        std::cout << "  make " << name_ << '\n';
    }
    ~Noisy() { std::cout << "  drop " << name_ << '\n'; }
    Noisy(const Noisy &) = delete;
    Noisy &operator=(const Noisy &) = delete;

private:
    std::string name_;
};
