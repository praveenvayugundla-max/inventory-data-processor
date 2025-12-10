from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# create db and migrate objects
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # basic config (you can update DB URL later)
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "postgresql+psycopg2://postgres:70722109@localhost:5432/inventory_db"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
