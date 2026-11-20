# capture: session copy=people_sort.rs,people.csv
rustc --edition 2021 -O people_sort.rs -o people_sort
./people_sort
