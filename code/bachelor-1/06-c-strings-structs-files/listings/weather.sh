# capture: session copy=weather_csv.c,weather.csv
gcc -std=c17 -O2 -Wall -Wextra weather_csv.c -o weather_csv
./weather_csv weather.csv
./weather_csv nosuchfile.csv; echo "exit status $?"
