import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    FLASK_RUN_HOST = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    FLASK_RUN_PORT = os.environ.get("FLASK_RUN_PORT", 5001)
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", True)

    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_NAME",
        f"sqlite:///{os.path.join(basedir, '../instance', 'anker_freiburg.db')}"
    )
    print(SQLALCHEMY_DATABASE_URI)
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_IDENTITY_CLAIM = "user_id"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)

    REGISTRATION_KEY = os.environ.get("REGISTRATION_CODE")

