from app.person.models import Person  # noqa
from app.person.schemas import PersonSchema  # noqa


def register_routes(api, app, root="api"):
    from app.person.controllers import api as udaconnect_person

    api.add_namespace(udaconnect_person, path=f"/{root}")