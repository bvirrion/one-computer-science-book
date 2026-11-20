# capture: session copy=loans.csv
export LC_ALL=C # hidden
head -3 loans.csv
tail -n +2 loans.csv | cut -d, -f3 | sort | uniq -c | sort -rn | head -5
tail -n +2 loans.csv | cut -d, -f3 | sort -u | wc -l
