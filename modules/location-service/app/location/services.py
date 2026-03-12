from datetime import datetime
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
        location.wkt_shape = coord_text

        # Emitir evento de 'lectura' (Audit Log)
        try:
            audit_data = {
                "action": "RETRIEVE",
                "location_id": location_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            producer.send('location-audit', audit_data)
        except Exception as e:
            logger.warning(f"No se pudo registrar la auditoría en Kafka: {e}")

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
                "lng": location["longitude"],
                "creation_time": new_location.creation_time.isoformat()

            }
            producer.send(
                "location-created",
                 key=str(new_location.person_id).encode(),
                value=event_data
            )
            producer.flush()
        except Exception as e:
            logger.error(f"Error enviando evento a Kafka: {e}")

        return new_location

