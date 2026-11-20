# capture: session copy=weather.csv
export LC_ALL=C # hidden
grep -q Hilltop weather.csv; echo $?
grep -c Harbour weather.csv; echo $?
ls weather.csv > /dev/null && false; echo $?
false || true; echo $?
