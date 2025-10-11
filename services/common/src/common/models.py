from datetime import datetime
from typing import List, Optional
from uuid import NAMESPACE_URL, uuid5

from pydantic import BaseModel


class Event(BaseModel):
    id: Optional[str] = None
    origin: str
    date: datetime
    band: List[str] = []
    location: Optional[str] = None
    price_eur: Optional[float] = None
    status_kind: Optional[str] = None
    new_location: Optional[str] = None
    status_raw: Optional[str] = None
    section: Optional[str] = None
    members: List[str] = []
    genres: List[str] = []

    def generate_id(self) -> str:
        band_name = self.band[0] if self.band else "unknown"
        location = self.location or "unknown"
        base = f"{self.date.isoformat()}::{band_name.lower()}::{location.lower()}"
        return str(uuid5(NAMESPACE_URL, base))
