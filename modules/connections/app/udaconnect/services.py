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
    
        connections: List[Connection] = db.session.query(Connection).join(Location).filter(
            Connection.person_id == person_id,
            Location.creation_time >= start_date,
            Location.creation_time < end_date
        ).all()

        person_ids = {conn.exposed_person_id for conn in connections}
        persons_map: Dict[int, Person] = {
            person.id: person
            for person in db.session.query(Person).filter(Person.id.in_(person_ids)).all()
        }

        for conn in connections:
            conn.person = persons_map.get(conn.exposed_person_id)
            conn.location = db.session.query(Location).get(conn.location_id)

        return connections

