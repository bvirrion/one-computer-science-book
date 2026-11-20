# capture: session copy=weather.csv,temps.h,temps.c,checksum_naive.c,checksum_fixed.c,checksum_ref.py
gcc -std=c17 -O2 -Wall -Wextra checksum_naive.c temps.c -lm -o naive
./naive weather.csv
gcc -std=c17 -O0 -fsanitize=undefined checksum_naive.c temps.c -lm -o naive_ub
./naive_ub weather.csv
gcc -std=c17 -O2 -Wall -Wextra checksum_fixed.c temps.c -lm -o fixed
./fixed weather.csv
python3 checksum_ref.py weather.csv
