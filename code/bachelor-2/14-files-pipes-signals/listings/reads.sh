# reads.sh: how many times does copy read in.txt, for each buffer size?
for b in 1 10 100 1000 4096 10000 65536; do
    strace -qq -e trace=read -P "$PWD/in.txt" -o r.txt ./copy in.txt out.txt "$b"
    echo "b = $b: $(wc -l < r.txt) reads"
done
