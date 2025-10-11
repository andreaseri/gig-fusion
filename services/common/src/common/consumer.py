from __future__ import annotations

import json
import logging

from common.config import settings
from confluent_kafka import Consumer, KafkaError, KafkaException

level = settings.LOG_LEVEL or "ERROR"
logging.basicConfig(level=getattr(logging, level))
logger = logging.getLogger(__name__)


class EventConsumer:
    """Shared Kafka/Redpanda consumer with graceful shutdown and callback support."""

    def __init__(
        self,
        group_id: str,
        topic: str | None = None,
        brokers: str | None = None,
        auto_offset_reset: str = "earliest",
        enable_auto_commit: bool = True,
    ):
        self.topic = topic or settings.EVENT_TOPIC
        self.brokers = brokers or settings.REDPANDA_BROKERS

        self.consumer = Consumer(
            {
                "bootstrap.servers": self.brokers,
                "group.id": group_id,
                "auto.offset.reset": auto_offset_reset,
                "enable.auto.commit": enable_auto_commit,
            }
        )

    def consume(self, callback, poll_timeout: float = 1.0):
        """Continuously poll messages and invoke callback(event_dict)."""
        logger.info(f"✅ Listening to topic '{self.topic}' on {self.brokers} ...")
        self.consumer.subscribe([self.topic])

        try:
            while True:
                msg = self.consumer.poll(poll_timeout)
                if msg is None:
                    logger.debug(f"⚠️  Waiting...")
                    continue
                if msg.error():
                    if msg.error().code() != KafkaError._PARTITION_EOF:
                        logger.error(f"⚠️  Consumer error: {msg.error()}")
                    continue

                try:
                    payload = json.loads(msg.value().decode("utf-8"))
                except KeyboardInterrupt:
                    logger.error(f"⚠️  KeyboardInterrupt detected, shutting down...")
                    break
                except Exception as e:
                    logger.error(f"⚠️  Failed to decode message: {e}")
                    continue

                callback(payload)
        except KafkaException as e:
            logger.error(f"❌ Kafka exception: {e}")
            pass
        except Exception as e:
            logger.error(f"⚠️  Unexpected error: {e}")
        finally:
            self.close()

    def close(self):
        """Cleanly close the consumer."""
        logger.info("🧹 Closing consumer connection...")
        try:
            self.consumer.close()
            logger.info("✅ Consumer closed.")
        except Exception as e:
            logger.error(f"⚠️  Error closing consumer: {e}")
