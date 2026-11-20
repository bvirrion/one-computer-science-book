# capture: session copy=weather.csv
export LC_ALL=C # hidden
ls weather.csv; echo "exit status $?"
ls nosuchfile.csv; echo "exit status $?"
grep -q Hilltop weather.csv && echo "Hilltop found"
grep -q Harbour weather.csv || echo "Harbour not found"
true; echo $?
false; echo $?
