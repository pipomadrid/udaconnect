import logging
from typing import Dict, List

from app import db
from app.person.models import Person
from app.person.schemas import PersonSchema

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("person-service")


class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        """Create a new person record."""
        validation_results: Dict = PersonSchema().validate(person)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        """Retrieve a person by ID."""
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        """Retrieve all persons."""
        return db.session.query(Person).all()
