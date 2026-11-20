# capture: session copy=exo_strcat.c
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
gcc -std=c17 -O0 -g -fsanitize=address exo_strcat.c -o exo_strcat
{ ./exo_strcat 2>&1 | grep -E "ERROR|WRITE|#[0-2] |is located|overflows"; } 2>/dev/null
