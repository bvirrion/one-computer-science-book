# capture: session copy=dict_table.rs,dict.rs,dict_bugs.rs,books.csv
cut -d, -f2 books.csv | tail -n +2 > titles.txt
rustc --edition 2021 -O dict.rs -o dict && ./dict < titles.txt
for b in bug1 bug2 bug3; do rustc --edition 2021 --cfg $b dict_bugs.rs 2>&1 | grep -m1 -A9 '^error\['; done
