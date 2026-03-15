import json
import os
import logging
from kafka import KafkaConsumer
from sqlalchemy.sql import text
from app import db
from app import create_app


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("location-consumer")

KAFKA_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'redpanda:9092')
TOPIC = "location-created"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="connection-service"
)


def process_location_event(event):
    person_id = event["person_id"]
    location_id = event["location_id"]
    latitude = event["latitude"]
    longitude = event["longitude"]

    query = text("""
        SELECT person_id
        FROM location
        WHERE ST_DWithin(
            coordinate::geography,
            ST_SetSRID(ST_MakePoint(:longitude, :latitude),4326)::geography,
            5
        )
        AND person_id != :person_id
    """)

    rows = db.engine.execute(
        query,
        latitude=latitude,
        longitude=longitude,
        person_id=person_id
    )

    for row in rows:
        exposed_person_id = row[0]

        try:
            insert_query = text("""
                INSERT INTO connection (person_id, exposed_person_id, location_id)
                VALUES (:person_id, :exposed_person_id, :location_id)
                ON CONFLICT DO NOTHING
            """)

            db.engine.execute(
                insert_query,
                person_id=person_id,
                exposed_person_id=exposed_person_id,
                location_id=location_id
            )

        except Exception as e:
            logger.warning(f"Error inserting connection: {e}")


def consume():
    logger.info("Starting Kafka consumer...")
    app = create_app()
    for message in consumer:
        event = message.value
        logger.info(f"Received event: {event}")
        
        with app.app_context():
            process_location_event(event)
