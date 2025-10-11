"""
scraper_common — shared components for scraper services.
Includes:
- Kafka producer (Redpanda compatible)
- Kafka consumer (Redpanda compatible)
- Config management
- Pydantic data models
"""

from .config import settings
from .consumer import EventConsumer
from .models import Event
from .producer import EventProducer

__all__ = ["EventProducer", "EventConsumer", "settings", "Event"]
