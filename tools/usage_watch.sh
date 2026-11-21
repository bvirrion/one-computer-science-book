#!/usr/bin/env bash
# Weekly-limit watcher of the CS fresh-reader run (main session; user rule 2026-11-21: pause at 40 %).
# Every 20 minutes: read the plan's weekly usage; at >= THRESHOLD % create sources/PAUSE
# (the readers stop before their next chapter). Never removes PAUSE: the main session does,
# after the reset. Log: sources/usage_watch.log. Stop it with: kill $(cat sources/usage_watch.pid)
set -u
cd "$(dirname "$0")/.."
TH=${THRESHOLD:-40}
echo $$ > sources/usage_watch.pid
while true; do
  line=$(claude -p /usage --tools '' 2>/dev/null | grep -m1 'Current week (all models)')
  pct=$(sed -n 's/.*: \([0-9]\+\)% used.*/\1/p' <<<"$line")
  echo "$(date -Is) ${pct:-?}% | $line" >> sources/usage_watch.log
  if [ -n "$pct" ] && [ "$pct" -ge "$TH" ] && [ ! -e sources/PAUSE ]; then
    echo "PAUSE created $(date -Is) at ${pct}% of the week (threshold ${TH}%)" > sources/PAUSE
    echo "$(date -Is) PAUSE created" >> sources/usage_watch.log
  fi
  sleep 1200
done
