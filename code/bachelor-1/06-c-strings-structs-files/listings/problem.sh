# capture: session copy=weather.h,weather_io.c,archive.c,weather.csv fixtimes
[ -z "$NORAND" ] && exec env -i NORAND=1 PATH=/usr/bin:/bin setarch "$(uname -m)" -R bash "$0" # hidden
gcc -std=c17 -O2 -Wall -Wextra archive.c weather_io.c -o archive -lm
./archive
ls -l weather.csv first.bin reading.bin packed.bin
od -A d -t x1 -N 32 first.bin
od -A d -t x1 -N 24 packed.bin
head -2 weather.csv
