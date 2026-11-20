# capture: session copy=last_seat.c,trim.sh
gcc -std=c17 -O1 -g -fsanitize=thread -o last_seat last_seat.c
setarch -R ./last_seat 2>&1 | bash trim.sh
