# capture: session fixtimes
export LC_ALL=C # hidden
echo "Hilltop, 212 m" > station.txt
ln station.txt copy.txt
ln -s station.txt shortcut.txt
ls -l
[ station.txt -ef copy.txt ] && echo "station.txt and copy.txt are the same file"
echo "Riverside, 48 m" >> copy.txt
cat station.txt
rm station.txt
ls -l
cat copy.txt
cat shortcut.txt
