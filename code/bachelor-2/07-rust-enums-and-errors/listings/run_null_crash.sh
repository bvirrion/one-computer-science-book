# capture: session copy=null_crash.c exit
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
gcc -std=c17 -O0 -g -fsanitize=address null_crash.c -o null_crash
./null_crash
