# capture: session copy=loans.hpp,loans_by_member.cpp,loans.csv
g++ -std=c++20 -O2 -Wall -Wextra loans_by_member.cpp -o loans_by_member
./loans_by_member loans.csv
