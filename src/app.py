from flask import Flask
from flask_cors import CORS
from extensions import db, jwt, ma, migrate
from config import Config


def create_app():
    # config
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True, origins=["http://localhost:5173", "https://anker-tattoo-piercing.vercel.app"])

    # initialization
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from auth.views import auth_blueprint
    from auth.routes import admin_blueprint
    app.register_blueprint(blueprint=auth_blueprint)
    app.register_blueprint(blueprint=admin_blueprint)

    # register app routes
    from routes import register_routes
    register_routes(app, db)

    return app
