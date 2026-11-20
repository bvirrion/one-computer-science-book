# capture: session copy=directory_server.c,directory.c,directory.h,servers.c,servers.h,net.c,net.h,directory_client.py,people.csv,streets.csv
gcc -std=c17 -O2 -Wall -Wextra -o directory_server *.c
./directory_server 44166 poll 4 &
sleep 0.2 # hidden
python3 directory_client.py 44166 "who 1" "who 4" "street Bridge Road" "where is 7"
wait
