from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(env=None):
    app = Flask(__name__)

    if env is None:
        app.config.from_object("app.config")
    else:
        app.config.from_object(env)

    db.init_app(app)

    # Register blueprints
    from app.person import routes

    app.register_blueprint(routes.api, url_prefix="/api")

    return app
