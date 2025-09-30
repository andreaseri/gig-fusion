import os
from typing import Any, Dict, Optional

import meilisearch


class MeiliClient:
    def __init__(self, index_name: str = "events") -> None:
        url = os.getenv("MEILI_URL", "http://localhost:7700")
        key = os.getenv("MEILI_API_KEY")
        self.client = meilisearch.Client(url, key)
        self.index = self.client.index(index_name)

    def search(self, q: str, opts: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        opts = opts or {}
        return self.index.search(q, opts)
