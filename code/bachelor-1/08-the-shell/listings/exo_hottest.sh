# capture: session copy=weather.csv
export LC_ALL=C # hidden
tail -n +2 weather.csv | grep -vE ',,|,-99' | sort -t, -k3,3gr | sort -t, -k2,2 -s -u
