import logging
from app import create_app
from app.person.models import Person
from app.person.services import PersonService
from protos import person_pb2, person_pb2_grpc

logger = logging.getLogger("person-service")

app = create_app()

class PersonServicer(person_pb2_grpc.PersonServiceServicer):
    """Implementation of PersonService gRPC service."""

    def GetPerson(self, request, context):
        """Get a person by ID."""
        try:
            with app.app_context():
                person: Person = PersonService.retrieve(request.id)
                if not person:
                    context.set_details("Person not found")
                    context.set_code(4)  # NOT_FOUND
                    return person_pb2.PersonReply()

                return person_pb2.PersonReply(
                    id=person.id,
                    first_name=person.first_name,
                    last_name=person.last_name,
                    company_name=person.company_name,
                )
        except Exception as e:
            logger.error(f"Error retrieving person: {str(e)}")
            context.set_details(f"Error retrieving person: {str(e)}")
            context.set_code(13)  # INTERNAL
            return person_pb2.PersonReply()

    def GetAllPersons(self, request, context):
        """Get all persons."""
        try:
            # Envolvemos el acceso a la base de datos en el contexto de la aplicación
            with app.app_context():
                persons = PersonService.retrieve_all()
                person_replies = [
                    person_pb2.PersonReply(
                        id=person.id,
                        first_name=person.first_name,
                        last_name=person.last_name,
                        company_name=person.company_name,
                    )
                    for person in persons
                ]
            return person_pb2.PersonList(persons=person_replies)
        except Exception as e:
            logger.error(f"Error retrieving persons: {str(e)}")
            context.set_details(f"Error retrieving persons: {str(e)}")
            context.set_code(13)  # INTERNAL
            return person_pb2.PersonList()

    def CreatePerson(self, request, context):
        """Create a new person."""
        try:
            with app.app_context():
                person_data = {
                    "first_name": request.first_name,
                    "last_name": request.last_name,
                    "company_name": request.company_name,
                }
                person: Person = PersonService.create(person_data)

                return person_pb2.PersonReply(
                    id=person.id,
                    first_name=person.first_name,
                    last_name=person.last_name,
                    company_name=person.company_name,
                )
        except Exception as e:
            logger.error(f"Error creating person: {str(e)}")
            context.set_details(f"Error creating person: {str(e)}")
            context.set_code(13)  # INTERNAL
            return person_pb2.PersonReply()
