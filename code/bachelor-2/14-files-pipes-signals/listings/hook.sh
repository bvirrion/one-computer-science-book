# capture: session copy=words.txt
tr -cs 'A-Za-z' '\n' < words.txt | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn | head -6
