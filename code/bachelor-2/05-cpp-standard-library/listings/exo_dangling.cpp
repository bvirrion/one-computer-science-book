// exo_dangling.cpp: a function that returns a lambda.
#include <cstdio>
#include <functional>
#include <string>

std::function<bool(const std::string &)> starts_with_street(const std::string &prefix)
{
    std::string p = prefix + " ";                           // "Orchard " and so on
    return [&p](const std::string &s) { return s.compare(0, p.size(), p) == 0; };
}

int main()
{
    std::setvbuf(stdout, nullptr, _IONBF, 0);
    auto is_orchard = starts_with_street("Orchard");
    std::printf("checking\n");
    std::printf("%d\n", is_orchard("Orchard Lane"));
    return 0;
}
