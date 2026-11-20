# capture: session copy=use_after_free.c exit
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
gcc -std=c17 -O0 -g -fsanitize=address use_after_free.c -o use_after_free
./use_after_free
