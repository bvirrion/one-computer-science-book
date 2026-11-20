# capture: session
export LC_ALL=C # hidden
printf 'Hilltop\nRiverside\nHilltop\nharbour\nHilltop\nRiverside\n' > visits.txt
sort visits.txt | uniq -c | sort -rn | head -2
uniq -c visits.txt | wc -l
tr a-z A-Z < visits.txt | sort -u
