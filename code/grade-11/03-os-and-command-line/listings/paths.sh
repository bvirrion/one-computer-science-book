# capture: session copy=books.csv
mkdir -p library/books library/members
mv books.csv library/books/
cd library/members
ls ../books
head -3 ../books/books.csv
realpath ../books/books.csv
cd ../../library/./books
pwd
