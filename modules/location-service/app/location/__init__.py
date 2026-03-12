from app.location.models import Location  # noqa
from app.location.schemas import LocationSchema  # noqa


def register_routes(api, app, root="api"):
    from app.location.controllers import api as udaconnect_location

    api.add_namespace(udaconnect_location, path=f"/{root}")