# capture: session copy=env_child.c
export LC_ALL=C # hidden
gcc -std=c17 -O2 -Wall env_child.c -o env_child
./env_child one "two words" 3; echo "exit status $?"
STATION=Hilltop ./env_child
STATION=Riverside
./env_child
export STATION
./env_child
