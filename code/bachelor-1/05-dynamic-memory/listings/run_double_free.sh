# capture: session copy=double_free.c
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
gcc -std=c17 -O0 -g -fsanitize=address double_free.c -o double_free
./double_free
