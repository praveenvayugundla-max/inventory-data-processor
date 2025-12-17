from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .models import db
from .routes import main
from .category_routes import category_bp

migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # App Config
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql+psycopg2://postgres:70722109@localhost:5432/inventory_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"  # change later

  
    # Initialize extensions
  
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

   
    # Register Blueprints
 
    app.register_blueprint(main)
    app.register_blueprint(category_bp)

   
    # Global Error Handlers (
 
    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(403)
    def forbidden(e):
        return {"error": "Forbidden"}, 403

    @app.errorhandler(500)
    def server_error(e):
        return {"error": "Internal server error"}, 500

    return app
