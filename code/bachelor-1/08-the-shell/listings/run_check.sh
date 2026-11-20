# capture: session copy=check_csv.sh,books.csv,loans.csv,members.csv,weather.csv
export LC_ALL=C # hidden
chmod +x check_csv.sh
./check_csv.sh *.csv; echo "exit status $?"
printf 'a,b\n1,2\n3\n' > broken.csv
./check_csv.sh broken.csv nosuch.csv; echo "exit status $?"
./check_csv.sh; echo "exit status $?"
