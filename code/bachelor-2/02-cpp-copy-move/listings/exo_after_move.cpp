// exo_after_move.cpp (exercise 6): a queue of jobs, emptied by mistake.
#include <iostream>
#include <string>
#include <utility>
#include <vector>

int main()
{
    std::vector<std::string> jobs = {"backup", "rotate logs", "send report"};
    std::vector<std::vector<std::string>> history;
    for (int day = 1; day <= 3; day++) {
        history.push_back(std::move(jobs));            // keep today's list
        std::cout << "day " << day << ": " << jobs.size() << " jobs\n";
    }
    std::cout << "history: " << history[0].size() << ' ' << history[1].size() << ' '
              << history[2].size() << '\n';
    return 0;
}
