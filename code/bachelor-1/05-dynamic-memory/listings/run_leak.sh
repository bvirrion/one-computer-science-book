# capture: session copy=leak.c
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
gcc -std=c17 -O1 -g -fsanitize=address leak.c -o leak
./leak
