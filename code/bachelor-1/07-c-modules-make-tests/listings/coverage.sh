# capture: session copy=classify.c,classify.h,classify_run.c,three.txt,all.txt
export LC_ALL=C # hidden
gcc -std=c17 -O0 --coverage -c classify.c
gcc -std=c17 -O0 classify_run.c classify.o --coverage -o classify_run
./classify_run < three.txt
gcov -b classify.c | sed -n 1,5p
grep -E "^ +[0-9#]+: +[0-9]+:" classify.c.gcov
sed -n 11,17p classify.c.gcov
rm classify.gcda
./classify_run < all.txt > /dev/null
gcov -b classify.c | sed -n 2,4p
