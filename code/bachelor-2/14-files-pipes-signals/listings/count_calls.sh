# capture: session copy=copy.c,reads.sh
gcc -O2 -o copy copy.c
head -c 100000 /dev/zero | tr '\0' 'x' > in.txt
bash reads.sh
cmp in.txt out.txt && echo same
