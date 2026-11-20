// invalidation.cpp: adding to a vector while a loop walks it.
#include <cstdio>
#include <vector>

int main()
{
    std::setvbuf(stdout, nullptr, _IONBF, 0);       // print at once: the sanitizer may stop the program
    std::vector<int> due{3, 8, 12, 20};             // days until due; full: capacity 4
    for (int d : due) {                            // the loop holds an iterator into the block
        std::printf("due in %d days\n", d);
        if (d > 10)
            due.push_back(d + 21);                  // renew the loan: the block may move
    }
    return 0;
}
