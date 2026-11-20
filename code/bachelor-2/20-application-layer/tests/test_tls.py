"""TLS on loopback: verification, the wrong name refused, 22 bytes per record."""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

LISTINGS = Path(__file__).resolve().parents[1] / "listings"


@pytest.mark.skipif(shutil.which("openssl") is None, reason="openssl is not installed")
def test_tls(tmp_path):
    subprocess.run(["openssl", "req", "-x509", "-newkey", "ec", "-pkeyopt",
                    "ec_paramgen_curve:prime256v1", "-nodes", "-days", "1",
                    "-keyout", "key.pem", "-out", "cert.pem", "-subj", "/CN=www.brenmoor.test",
                    "-addext", "subjectAltName=DNS:www.brenmoor.test"],
                   cwd=tmp_path, check=True, capture_output=True)
    out = {}
    for f in ("tls_echo.py", "tls_wrong_name.py", "tls_overhead.py"):
        out[f] = subprocess.run([sys.executable, LISTINGS / f], cwd=tmp_path, check=True,
                                capture_output=True, text=True).stdout
    assert "(verified)" in out["tls_echo.py"] and "HELLO FROM" in out["tls_echo.py"]
    assert out["tls_wrong_name.py"].startswith("refused: Hostname mismatch")
    rows = out["tls_overhead.py"].splitlines()[2:]
    assert len(rows) == 6 and all(r.split()[-1] == "22" for r in rows)
