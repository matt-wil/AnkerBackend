import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from passlib.context import CryptContext

db = SQLAlchemy()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
jwt = JWTManager()


def create_app():
    # config
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    jwt_secret_key = os.environ.get("JWT_SECRET_KEY")
    jwt_token_location = ["headers"]
    jwt_identity_claim = "user_id"
    CORS(app, origins="http://localhost:5173")

    # initiation
    db.init_app(app)
    jwt.init_app(app)

    # imports
    from routes import register_routes
    register_routes(app, db)
    migrate = Migrate(app, db)

    return app
