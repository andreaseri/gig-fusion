from dateutil import parser as dateparser

def clean_event(ev):
    # Normalize minimal fields
    out = dict(ev)
    if "date" in out and out["date"]:
        try:
            out["date"] = dateparser.parse(out["date"]).isoformat()
        except Exception:
            pass
    return out
