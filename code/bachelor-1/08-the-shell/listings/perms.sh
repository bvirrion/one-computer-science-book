# capture: session fixtimes
export LC_ALL=C # hidden
umask 022 # hidden
echo "rain" > notes.txt
ls -l notes.txt
chmod go-r notes.txt
ls -l notes.txt
chmod 640 notes.txt
ls -l notes.txt
chmod u-w notes.txt
bash -c 'echo "more rain" >> notes.txt'
mkdir box
chmod 711 box
ls -ld box
umask
