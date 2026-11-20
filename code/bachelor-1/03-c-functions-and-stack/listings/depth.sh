# capture: session copy=deep.c
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
gcc -std=c17 -O0 deep.c -o deep
ulimit -s
(ulimit -s 512; ./deep > log.txt) 2>/dev/null; echo "exit status $?"
head -n 3 log.txt
tail -n 1 log.txt
for kib in 256 1024 2048; do (ulimit -s $kib; ./deep > log.txt) 2>/dev/null; tail -n 1 log.txt; done
