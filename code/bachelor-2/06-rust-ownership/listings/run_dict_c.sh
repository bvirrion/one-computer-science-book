# capture: session copy=dict.h,dict.c,books.csv exit
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
cut -d, -f2 books.csv | tail -n +2 > titles.txt
gcc -std=c17 -O0 -g -fsanitize=address dict.c -o dict && ./dict < titles.txt
gcc -std=c17 -O0 -g -fsanitize=address -DBUG=1 dict.c -o dict1 && ./dict1 < titles.txt
gcc -std=c17 -O0 -g -fsanitize=address -DBUG=2 dict.c -o dict2 && ./dict2 < titles.txt
gcc -std=c17 -O0 -g -fsanitize=address -DBUG=3 dict.c -o dict3 && ./dict3 < titles.txt
