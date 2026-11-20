# capture: session copy=library.hpp,library_demo.cpp,books.csv,loans.csv
g++ -std=c++20 -O2 -Wall -Wextra library_demo.cpp -o library_demo
./library_demo books.csv loans.csv
