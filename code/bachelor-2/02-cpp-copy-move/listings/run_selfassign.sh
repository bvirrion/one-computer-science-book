# capture: session copy=exo_selfassign.cpp exit
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
g++ -std=c++20 -O0 -g -fsanitize=address exo_selfassign.cpp -o exo_selfassign
./exo_selfassign
