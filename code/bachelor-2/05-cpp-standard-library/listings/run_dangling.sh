# capture: session copy=exo_dangling.cpp exit
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
g++ -std=c++20 -O0 -g -fsanitize=address exo_dangling.cpp -o exo_dangling
ASAN_OPTIONS=detect_stack_use_after_return=1 ./exo_dangling
