# capture: session copy=weather.csv
export LC_ALL=C # hidden
grep -c Riverside weather.csv
grep -E ',Riverside,2[4-9]\.' weather.csv
grep -E ',,|-99' weather.csv
sed -n 2,3p weather.csv
sed 's/,/;/g' weather.csv | head -2
sed -E 's/^([0-9]{4})-([0-9]{2})-([0-9]{2})/\3.\2.\1/' weather.csv | sed -n 2,3p
