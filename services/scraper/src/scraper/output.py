import json
import os
from datetime import datetime
from typing import Optional


def save_events(events, basepath: str = "concert_events", path: Optional[str] = None) -> str:
    """Save events to a timestamped JSON file.

    - basepath: base filename used when `path` is a directory or not provided.
    - path: optional. If a file path is provided (endswith .json) it will be used
      directly. If a directory path is provided, the file will be created inside
      that directory using the basepath + timestamp. If omitted, file is created
      in current working directory.

    Returns the full path to the written file.
    """
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    if path:
        # If user passed a directory, create file inside it
        if os.path.isdir(path) or path.endswith(os.path.sep):
            os.makedirs(path, exist_ok=True)
            filename = os.path.join(path, f"{basepath}_{ts}.json")
        else:
            # treat path as a file path; ensure parent dir exists
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            # if path has no .json extension, append timestamp
            if not path.lower().endswith('.json'):
                filename = f"{path}_{ts}.json"
            else:
                filename = path
    else:
        filename = f"{basepath}_{ts}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(events)} events to {filename}")
    return filename
