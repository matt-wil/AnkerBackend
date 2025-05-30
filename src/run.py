from app import create_app

flask_app = create_app()

if __name__ == '__main__':
    flask_app.run(
        host=flask_app.config.get("FLASK_RUN_HOST"),
        port=flask_app.config.get("FLASK_RUN_PORT"),
        debug=flask_app.config.get("FLASK_DEBUG"))
