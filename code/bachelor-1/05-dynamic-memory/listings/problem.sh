# capture: session copy=phonebook.h,phonebook_v0.c,pbdemo.c
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
gcc -std=c17 -O1 -g -fsanitize=address -fsanitize-recover=address pbdemo.c phonebook_v0.c -o pb
ASAN_OPTIONS=halt_on_error=0 ./pb > report.txt 2>&1
sed -n 2,6p report.txt
grep -E "^SUMMARY|^Emil|^removed|contacts$" report.txt
