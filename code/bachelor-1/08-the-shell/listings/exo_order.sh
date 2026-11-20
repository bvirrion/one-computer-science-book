# capture: session
export LC_ALL=C # hidden
ls nosuchfile > out1.txt 2>&1
cat out1.txt
ls nosuchfile 2>&1 > out2.txt
cat out2.txt
