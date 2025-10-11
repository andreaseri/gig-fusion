import logging

import meilisearch.client
import meilisearch.errors
from common import Event, EventConsumer, settings

level = settings.LOG_LEVEL or "ERROR"
logging.basicConfig(level=getattr(logging, level))
logger = logging.getLogger(__name__)

client = meilisearch.client.Client(
    settings.MEILISEARCH_URL, settings.MEILISEARCH_API_KEY
)
index = client.index("events")


def upsert_event(event: Event):
    try:
        event.id = event.generate_id()
        doc = index.get_document(event.id)

        logger.debug(f"Existing doc: {doc.origin}")
        logger.debug(f"New event: {event.origin}")

        if doc and len(event.band) > len(doc.band):
            index.update_documents([event.model_dump(mode="json")])
            logger.debug(f"Updated event: {event.id}")

    except meilisearch.errors.MeilisearchApiError as e:
        if e.code == "document_not_found":
            index.add_documents([event.model_dump(mode="json")])
            logger.debug(f"Inserted event: {event.id}")
        else:
            logger.error(f"MeiliSearch API error: {e}")
    except Exception as e:
        logger.error(f"Error upserting event: {e}")


def handle_event(data: dict):
    event = Event(**data)
    logger.info(f"📥 Received: {event.origin[:60]}")
    upsert_event(event)


consumer = EventConsumer(group_id="reindexer")
logger.info("EventConsumer created")
consumer.consume(handle_event)
logger.info("Shutting down consumer...")
