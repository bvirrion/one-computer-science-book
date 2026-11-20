# capture: session copy=uaf.c
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
gcc -std=c17 -O0 -g -fsanitize=address uaf.c -o uaf
./uaf
