# capture: session copy=make_log.py,log_check.py,logstat.sh
export LC_ALL=C # hidden
python3 make_log.py > access.log
wc -l access.log
head -3 access.log
grep status=error access.log | head -2
cut -d" " -f4 access.log | sort | uniq -c
grep -c status=error access.log
grep -E "^.{11}1[23]:" access.log | wc -l
grep status=error access.log | sed -E "s/.*reason=//" | sort | uniq -c | sort -rn
cut -c12-13 access.log | sort | uniq -c | sort -rn | head -3
grep -oE "member=[0-9]+" access.log | sort -u | wc -l
grep -c "member=-" access.log
python3 log_check.py access.log
chmod +x logstat.sh
./logstat.sh access.log 10; echo "exit status $?"
./logstat.sh access.log 07; echo "exit status $?"
./logstat.sh access.log 7am; echo "exit status $?"
