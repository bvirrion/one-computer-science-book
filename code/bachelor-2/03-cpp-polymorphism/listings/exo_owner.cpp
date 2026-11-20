// exo_owner.cpp (exercise 2): smart pointers, and still an error.
// capture: cflags=-O0 -g -fsanitize=address exit
#include <cstdio>
#include <memory>
#include <vector>

struct Sensor {
    ~Sensor() {}
    int id = 0;
};
struct LoggingSensor : Sensor {
    std::vector<double> history = std::vector<double>(1000, 0.0);
};

int main()
{
    std::vector<std::unique_ptr<Sensor>> sensors;
    sensors.push_back(std::make_unique<Sensor>());
    sensors.push_back(std::make_unique<LoggingSensor>());
    std::printf("%zu sensors\n", sensors.size());
    std::fflush(stdout);
    return 0;
}
