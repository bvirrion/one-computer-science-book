# capture: session copy=count_lines.sh,members.csv
export LC_ALL=C # hidden
cp members.csv "members 2024.csv"
bash count_lines.sh
