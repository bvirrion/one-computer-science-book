"""acl.py -- the toy app's access-control matrix, read by columns as access-control
lists and by rows as capabilities; then a confused deputy: the app's export service
writes a report to a file the caller names, with the app's own rights."""

MATRIX = {  # subject -> object -> rights
    "ada": {"loans.csv": "r", "ada-notes.txt": "rw"},
    "eve": {"loans.csv": "r", "eve-notes.txt": "rw"},
    "export-service": {
        "loans.csv": "r",
        "fines.csv": "rw",
        "ada-notes.txt": "w",
        "eve-notes.txt": "w",
    },
}

acls = {}  # object -> {subject: rights}: the columns, stored with each file
for subject, row in MATRIX.items():
    for obj, rights in row.items():
        acls.setdefault(obj, {})[subject] = rights
print("ACL of fines.csv:", acls["fines.csv"])
print("capabilities of eve:", MATRIX["eve"])  # a row, held by the subject


def may(subject, obj, right):
    return right in acls.get(obj, {}).get(subject, "")


def export_confused(caller, out):
    """Checks the service's own right to write `out`, not the caller's."""
    if not may("export-service", out, "w"):
        return "refused"
    return f"report written to {out}"


def export_fixed(caller, out):
    """Acts for the caller: both the service and the caller must hold the right."""
    if not (may("export-service", out, "w") and may(caller, out, "w")):
        return "refused"
    return f"report written to {out}"


for out in ("eve-notes.txt", "fines.csv"):
    print(f"eve asks for {out}:")
    print(
        f"   confused: {export_confused('eve', out)}; fixed: {export_fixed('eve', out)}"
    )
