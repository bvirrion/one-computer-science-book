# capture: session fixtimes
echo 'opens at nine' > hours.txt
ln hours.txt opening.txt
ln -s hours.txt shortcut.txt
ls -l
rm hours.txt
cat opening.txt
cat shortcut.txt
ls -l
