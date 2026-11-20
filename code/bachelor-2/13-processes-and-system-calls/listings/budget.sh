# capture: session copy=minish.c,minish_parse.c,minish_parse.h
gcc -o minish minish.c minish_parse.c
echo 'echo hi' > one.txt
PATH=/usr/bin strace -f -c -S name -o summary.txt ./minish < one.txt > /dev/null
awk '$1 !~ /^(%|-)/ { printf "%5d %4s  %s\n", $4, NF == 6 ? $5 : "", $NF }' summary.txt
: > none.txt
PATH=/usr/bin strace -f -c -o empty.txt ./minish < none.txt > /dev/null
awk '$NF == "total" { print $4, "calls for an empty script" }' empty.txt
PATH=/usr/bin strace -f -c -o alone.txt echo hi > /dev/null
awk '$NF == "total" { print $4, "calls for echo run alone" }' alone.txt
