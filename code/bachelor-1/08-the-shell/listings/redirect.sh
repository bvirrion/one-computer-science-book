# capture: session copy=weather.csv
export LC_ALL=C # hidden
ls weather.csv nosuchfile.csv > out.txt
cat out.txt
ls weather.csv nosuchfile.csv > out.txt 2> err.txt
cat err.txt
ls weather.csv nosuchfile.csv > all.txt 2>&1
cat all.txt
echo "first line" > notes.txt
echo "second line" >> notes.txt
cat notes.txt
wc -l < weather.csv
