# capture: session copy=hello_write.c
gcc -o hello hello_write.c
./hello
strace -qq -e trace=write,exit_group ./hello > /dev/null
