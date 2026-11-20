# capture: session copy=toy_login.c,toy_login_fixed.c
count() { objdump -d --no-show-raw-insn x | awk '/<main>:/,/^$/' | grep -c '^ '; }
build() { gcc -std=c17 -O2 $2 $1 -o x && printf '%-18s %-22s main: %3d instructions, file %6d bytes\n' $1 $2 $(count) $(stat -c %s x); }
build toy_login.c -fno-stack-protector
build toy_login.c -fstack-protector-all
build toy_login_fixed.c -fno-stack-protector
build toy_login.c -fsanitize=address
