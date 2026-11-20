# capture: session fixtimes
export LC_ALL=C # hidden
umask 022 # hidden
touch f
chmod 640 f; ls -l f
chmod 755 f; ls -l f
chmod 604 f; ls -l f
chmod 640 f; chmod u+x,o+r f; ls -l f
