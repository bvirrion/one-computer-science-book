# capture: session copy=twice.hpp,twice.cpp,main_twice.cpp exit
g++ -std=c++20 -c twice.cpp
g++ -std=c++20 -c main_twice.cpp
g++ twice.o main_twice.o -o twice
