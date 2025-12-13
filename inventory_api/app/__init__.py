from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .category_routes import category_bp

from .models import db
from .routes import main


migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # App Config
    
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql+psycopg2://postgres:70722109@localhost:5432/inventory_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"   # Change later for production

    # Initialize extensions
    
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register Blueprints
   
    app.register_blueprint(main)
    app.register_blueprint(category_bp)


    return app
