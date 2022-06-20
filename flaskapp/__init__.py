from flask import Flask

from flaskapp.config import DevelopmentConfig
from flaskapp.extensions import cache
from flaskapp.home.routes import home


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    app.register_blueprint(home)

    cache.init_app(app)

    return app
