# capture: session copy=invalidation.cpp exit
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
g++ -std=c++20 -O0 -g -fsanitize=address invalidation.cpp -o invalidation
./invalidation
