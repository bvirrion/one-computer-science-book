from datetime import date

import dateset_list
import dateset_set

for ds in [dateset_list, dateset_set]:
    holidays = ds.empty()
    for text in ["2026-01-01", "2026-05-01", "2026-12-25", "2026-05-01"]:
        ds.add(holidays, date.fromisoformat(text))
    print(ds.__name__, "size", ds.size(holidays),
          "| 25 December:", ds.contains(holidays, date(2026, 12, 25)),
          "| 24 December:", ds.contains(holidays, date(2026, 12, 24)))
