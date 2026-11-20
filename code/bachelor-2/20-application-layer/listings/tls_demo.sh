# capture: session copy=tls_echo.py,tls_wrong_name.py,tls_overhead.py
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -nodes -days 1 -keyout key.pem -out cert.pem -subj /CN=www.brenmoor.test -addext subjectAltName=DNS:www.brenmoor.test 2>/dev/null # hidden
python3 tls_echo.py
python3 tls_wrong_name.py
python3 tls_overhead.py
