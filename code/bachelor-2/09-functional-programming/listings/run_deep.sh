# capture: session copy=deep_recursion.rs exit
rustc --edition 2021 -C opt-level=0 deep_recursion.rs -o deep_recursion
sh -c './deep_recursion 2> err.txt; exit $?' 2> /dev/null; echo "exit status $?"
grep . err.txt | head -2 | sed 's/ ([0-9]*)//'
rustc --edition 2021 -C opt-level=3 deep_recursion.rs -o deep_recursion_o3
sh -c './deep_recursion_o3 2> err.txt; exit $?' 2> /dev/null; echo "exit status $?"
