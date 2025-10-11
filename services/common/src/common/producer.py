from __future__ import annotations

import json
import logging

from common.models import Event
from confluent_kafka import Producer

from .config import settings

level = settings.LOG_LEVEL or "ERROR"
logging.basicConfig(level=getattr(logging, level))
logger = logging.getLogger(__name__)


class EventProducer:
    """Kafka/Redpanda producer for event messages."""

    def __init__(self, brokers: str | None = None, topic: str | None = None):
        self.topic = topic or settings.EVENT_TOPIC
        self.brokers = brokers or settings.REDPANDA_BROKERS

        config = {
            "bootstrap.servers": self.brokers,
            "reconnect.backoff.ms": settings.KAFKA_RECONNECT_BACKOFF_MS,
            "reconnect.backoff.max.ms": settings.KAFKA_RECONNECT_BACKOFF_MS * 5,
            "delivery.timeout.ms": settings.KAFKA_DELIVERY_TIMEOUT_MS,
            "retries": settings.KAFKA_MAX_RETRIES,
            "retry.backoff.ms": 1000,
            "retry.backoff.max.ms": 5000,
        }
        logger.info(f"Connecting to Redpanda at {config} on topic '{self.topic}'")
        self.producer = Producer(config)

    def send(self, event: dict | Event):
        """Send event data (dict or Event model) to Redpanda."""
        payload = (
            event.model_dump_json()
            if hasattr(event, "model_dump_json")
            else json.dumps(event)
        )
        self.producer.produce(self.topic, payload.encode("utf-8"))
        self.producer.poll(10000)
        self.producer.flush()

    def close(self):
        """Flush and close the producer."""
        self.producer.flush()
