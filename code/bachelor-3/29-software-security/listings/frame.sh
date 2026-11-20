# capture: session copy=toy_login.c
gcc -std=c17 -O0 -fno-stack-protector -c toy_login.c -o plain.o
objdump -d --no-show-raw-insn plain.o | grep -A9 '<check>:' | grep 'rbp)' | cut -f2-
gcc -std=c17 -O0 -fstack-protector-all -c toy_login.c -o canary.o
objdump -d --no-show-raw-insn canary.o | grep -A16 '<check>:' | grep 'rbp)' | cut -f2-
