import logging
from datetime import datetime, timedelta
import os
from typing import Dict, List

from app import db
from app.protos import person_pb2, person_pb2_grpc
import grpc
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema
from sqlalchemy.sql import text

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")


class ConnectionService:
    @staticmethod
    def _get_grpc_persons():
        person_host = os.getenv("PERSON_SERVICE_HOST", "localhost")
        person_port = os.getenv("PERSON_SERVICE_GRPC_PORT", "5005")
        
        try:
            channel = grpc.insecure_channel(f"{person_host}:{person_port}")
            stub = person_pb2_grpc.PersonServiceStub(channel)
            persons_reply = stub.GetAllPersons(person_pb2.Empty())
            
            # Convert gRPC response to dict of {person_id: person_data}
            person_map = {}
            for person in persons_reply.persons:
                person_map[person.id] = {
                    "id": person.id,
                    "first_name": person.first_name,
                    "last_name": person.last_name,
                    "company_name": person.company_name,
                }
            
            channel.close()
            return person_map
        except Exception as e:
            logger.error(f"Error fetching persons via gRPC: {str(e)}")
            raise



    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
    
        person_map: Dict[str, Person] = ConnectionService._get_grpc_persons()

        query = text("""
            SELECT c.exposed_person_id,
                l.id,
                ST_X(l.coordinate),
                ST_Y(l.coordinate),
                l.creation_time
            FROM connection c
            JOIN location l ON c.location_id = l.id
            WHERE c.person_id = :person_id
            AND l.creation_time >= :start_date
            AND l.creation_time <= :end_date
        """)
        
        result: List[Connection] = []

        rows = db.engine.execute(
            query,
            person_id=person_id,
            start_date=start_date,
            end_date=end_date
        )   

        for exposed_person_id, location_id, lat, lng, time in rows:

            location = Location(
                id=location_id,
                person_id=exposed_person_id,
                creation_time=time
            )
            location.set_wkt_with_coords(lat, lng)

            result.append(
            Connection(
                person=person_map[exposed_person_id],
                location=location
            )
        )
            
        return result

