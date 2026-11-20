# capture: session copy=never_ends.toy exit
python -m toymachine run never_ends.toy > printed.txt
wc -l printed.txt
tail -n 3 printed.txt
