# capture: session copy=config.h,limits_main.c,stale.Makefile
export LC_ALL=C # hidden
make -f stale.Makefile && ./limits
sed -i "s/MAX_LOANS 3/MAX_LOANS 5/" config.h
make -f stale.Makefile && ./limits
