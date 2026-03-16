from typing import List

from app.person.models import Person
from app.person.schemas import PersonSchema
from app.person.services import PersonService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

api = Namespace("Person", description="Person management service.")  # noqa


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        """Create a new person."""
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        """Retrieve all persons."""
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<int:person_id>")
@api.param("person_id", "Unique identifier of the person")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id: int) -> Person:
        """Retrieve a person by ID."""
        person: Person = PersonService.retrieve(person_id)
        return person
