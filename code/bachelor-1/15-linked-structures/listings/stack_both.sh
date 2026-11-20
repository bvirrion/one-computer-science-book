# capture: session copy=stack.h,stack_array.c,stack_list.c,brackets.c
gcc -std=c17 -O2 -Wall -Wextra brackets.c stack_array.c -o check_array
gcc -std=c17 -O2 -Wall -Wextra brackets.c stack_list.c -o check_list
./check_array
./check_list
