# capture: session copy=books.csv
echo "first line" > log.txt
echo "second line" >> log.txt
cat log.txt
echo "a new start" > log.txt
cat log.txt
wc -l < books.csv
head -1 books.csv > header.txt
cat header.txt
