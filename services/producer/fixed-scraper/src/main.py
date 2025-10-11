import json
import logging

from common import Event, EventProducer, settings

level = settings.LOG_LEVEL or "ERROR"
logging.basicConfig(level=getattr(logging, level))
logger = logging.getLogger(__name__)

# event = Event(
#     origin="Foo at Club Berlin",
#     date="2025-10-09T20:00:00",
#     band=["Foo"],
#     location="Berlin"
# )

producer = EventProducer()
logger.info("EventProducer created")
# producer.send(event)

# load json file and send each event
with open("mock_concert_events.json", "r") as f:
    events = json.load(f)
    for event in events:
        event = Event(**event)
        producer.send(event)
        logger.debug(f"📤 Sent: {event.origin[:60]}")

producer.close()
logger.info("Shutting down producer...")
