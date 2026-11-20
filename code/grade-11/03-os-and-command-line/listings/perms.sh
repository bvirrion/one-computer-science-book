# capture: session fixtimes copy=books.csv
mkdir notes
echo "top secret" > notes/secret.txt
ls -l
chmod 640 books.csv
chmod u-r notes/secret.txt
ls -l books.csv notes/secret.txt
cat notes/secret.txt
chmod u+r notes/secret.txt
cat notes/secret.txt
