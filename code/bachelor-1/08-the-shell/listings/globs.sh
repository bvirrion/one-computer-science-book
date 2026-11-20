# capture: session fixtimes
export LC_ALL=C # hidden
touch a.csv b.csv notes.txt "rain 2025.csv"
ls
echo *.csv
echo ?.csv
echo [ab].csv
echo *.xml
echo "*.csv" '*.csv'
echo {a,b,c}.csv
