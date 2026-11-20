# capture: session copy=loans.csv
head -3 loans.csv
cut -d, -f3 loans.csv | head -3
cut -d, -f3 loans.csv | tail -n +2 | sort | uniq -c | sort -n | tail -3
grep -c ',$' loans.csv
