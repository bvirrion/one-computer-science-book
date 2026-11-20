# capture: session
getconf -a | grep -E 'LEVEL[123]_D?CACHE_(SIZE|ASSOC|LINESIZE)'
