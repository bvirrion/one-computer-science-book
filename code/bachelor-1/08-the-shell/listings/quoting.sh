# capture: session fixtimes
export LC_ALL=C # hidden
touch "rain 2025.csv"
f="rain 2025.csv"
ls $f
ls "$f"
printf '[%s]\n' $f
printf '[%s]\n' "$f"
echo "the file is $f" 'the file is $f' \$f
n=3; echo "$n files" "${n}0 files" "$n0 files"
