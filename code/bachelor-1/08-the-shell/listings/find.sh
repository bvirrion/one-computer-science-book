# capture: session copy=books.csv,loans.csv,weather.csv,members.csv
export LC_ALL=C # hidden
mkdir -p town/library town/weather town/old
mv books.csv loans.csv members.csv town/library/
mv weather.csv town/weather/
touch town/old/notes.txt
find town -type d | sort
find town -name '*.csv' | sort
find town -name '*.csv' -size +10k | sort
find town -name '*.csv' -exec wc -l {} + | sort -n
