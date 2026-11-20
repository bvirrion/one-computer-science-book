# capture: session copy=books.csv
mkdir backup
cp books.csv backup/books-copy.csv
ls backup
mv backup/books-copy.csv backup/old-books.csv
ls backup
rm backup/old-books.csv
ls backup
rmdir backup
ls
