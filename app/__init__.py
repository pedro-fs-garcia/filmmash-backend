from flask import Flask
from .build_database import init_db

def create_app():
    app = Flask(__name__)

    init_db()

    from .routes.main_routes import main
    app.register_blueprint(main)

    return app