import logging
from typing import Dict
from kafka import KafkaProducer
from app import db
import json
import os
from geoalchemy2.functions import ST_AsText, ST_Point
from sqlalchemy.sql import text
from app.location.models import Location
from app.location.schemas import LocationSchema

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("location-service")

# Configuración básica del productor (debería ir en una configuración global)
producer = KafkaProducer(
    bootstrap_servers=[os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka-broker:9092')],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class LocationService:
    @staticmethod
    def retrieve(location_id) -> Location:
        location, coord_text = (
            db.session.query(Location, Location.coordinate.ST_AsText())
            .filter(Location.id == location_id)
            .one()
        )

        # Rely on database to return text form of point to reduce overhead of conversion in app code
        location.wkt_shape = coord_text
        return location

    @staticmethod
    def create(location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        db.session.add(new_location)
        db.session.commit()

        try:
            event_data = {
                "location_id": new_location.id,
                "person_id": new_location.person_id,
                "lat": location["latitude"],
                "lng": location["longitude"]
            }
            producer.send('location-created', event_data)
            producer.flush()
        except Exception as e:
            logger.error(f"Error enviando evento a Kafka: {e}")

        return new_location

