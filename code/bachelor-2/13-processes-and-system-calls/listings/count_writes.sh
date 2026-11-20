# capture: session copy=lines.c
gcc -O2 -o lines lines.c
strace -qq -e trace=write -o b.txt ./lines 1000 > /dev/null; wc -l < b.txt
strace -qq -e trace=write -o u.txt ./lines 1000 unbuffered > /dev/null; wc -l < u.txt
