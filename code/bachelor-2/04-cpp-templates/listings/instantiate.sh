# capture: session copy=vec.hpp,vec_demo.cpp
g++ -std=c++20 -O0 -c vec_demo.cpp -o vec_demo.o
nm -C vec_demo.o | grep -c ' Vec<'
nm -C vec_demo.o | grep 'push_back'
