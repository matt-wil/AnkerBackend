from flask import request, jsonify
from .models import Booking, Client, Artist, Service, PortfolioImage


def register_routes(app, db):

    @app.route('/', methods=['GET'])
    def index():
        return f"<h1>Welcome to Anker Freiburg Database API<h1>"

    @app.route('/api', methods=['GET'])
    def get_all():
        bookings = Booking.query.all()
        bookings_to_dict = [booking.to_dict() for booking in bookings]
        clients = Client.query.all()
        clients_to_dict = [client.to_dict() for client in clients]
        artists = Artist.query.all()
        artists_to_dict = [artist.to_dict() for artist in artists]
        services = Service.query.all()
        services_to_dict = [service.to_dict() for service in services]
        portfolio_images = PortfolioImage.query.all()
        portfolio_images_to_dict = [portfolio_image.to_dict() for portfolio_image in portfolio_images]
        return jsonify(
            {
                'bookings': bookings_to_dict,
                'clients': clients_to_dict,
                'artists': artists_to_dict,
                'services': services_to_dict,
                'portfolio_images': portfolio_images_to_dict
            }
        ), 200

    @app.route('/api/bookings', methods=['GET', 'POST'])
    def handle_bookings():
        if request.method == 'GET':
            bookings = Booking.query.all()
            bookings_to_dict = [booking.to_dict() for booking in bookings]
            return jsonify(bookings_to_dict), 200

        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({"Error": "No Booking Data Found"}, 400)
            try:
                new_booking = Booking(**data)
                db.session.add(new_booking)
                db.session.commit()
                return jsonify(new_booking.to_dict(), 201)
            except Exception as e:
                db.session.rollback()
                return jsonify({"Error": f"Could not create item: {str(e)}"}, 400)

    @app.route('/api/bookings/<int:booking_id>', methods=['GET', 'PUT', 'DELETE'])
    def handle_booking(booking_id):
        booking = Booking.query.get_or_404(booking_id)
        if request.method == 'GET':
            return jsonify(booking.to_dict()), 200
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({"Error": "No data provided"}), 400
            try:
                for key, value in data.items():
                    setattr(booking, key, value)
                db.session.commit()
                return jsonify(booking.to_dict(), 200)
            except Exception as e:
                return jsonify({"Error": f"Could not update the booking: {str(e)}"})
        elif request.method == "DELETE":
            db.session.delete(booking)
            db.session.commit()
            return jsonify({"Success": "Item successfully deleted"}, 200)

    @app.route('/api/clients', methods=['GET'])
    def get_clients():
        clients = Client.query.all()
        clients_to_dict = [client.to_dict() for client in clients]
        return jsonify(clients_to_dict), 200

    @app.route('/api/artists', methods=['GET', 'POST'])
    def handle_artists():
        if request.method == "GET":
            artists = Artist.query.all()
            artists_to_dict = [artist.to_dict() for artist in artists]
            return jsonify(artists_to_dict), 200

        elif request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"Error": "No Artist Data Found"}), 400
            try:
                new_artist = Artist(**data)
                db.session.add(new_artist)
                db.session.commit()
                return jsonify(new_artist.to_dict()), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"Error": f"Error creating new Artist: {str(e)}"})

    @app.route('/api/artists/<int:artist_id>', methods=["GET", "PUT", "DELETE"])
    def handle_artist(artist_id):
        artist = Artist.query.get_or_404(artist_id)
        if request.method == 'GET':
            return jsonify(artist.to_dict()), 200
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({"Error": "No Artist data provided"}), 400
            try:
                for key, value in data.items():
                    setattr(artist, key, value)
                db.session.commit()
                return jsonify(artist.to_dict()), 200
            except Exception as e:
                return jsonify({"Error": f"Could not update the Artist: {str(e)}"}), 400
        elif request.method == "DELETE":
            db.session.delete(artist)
            db.session.commit()
            return jsonify({"Success": "Item successfully deleted"}), 200

    @app.route('/api/portfolio_images', methods=['GET', 'POST'])
    def handle_portfolio_images():
        if request.method == 'GET':
            portfolio_images = PortfolioImage.query.all()
            portfolio_images_to_dict = [portfolio_image.to_dict() for portfolio_image in portfolio_images]
            return jsonify(portfolio_images_to_dict), 200

        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({"Error": "Portfolio image data not received."}), 400
            try:
                new_portfolio_image = PortfolioImage(**data)
                db.session.add(new_portfolio_image)
                db.session.commit()
                return jsonify(new_portfolio_image.to_dict()), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"Error": f"Error creating new portfolio image {str(e)}"}), 400

    @app.route('/api/portfolio_images/<int:image_id>', methods=['GET', 'PUT', 'DELETE'])
    def handle_portfolio_image(image_id):
        portfolio_image = PortfolioImage.query.get_or_404(image_id)
        if request.method == 'GET':
            return portfolio_image
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({"Error", "No Data received"}), 400
            try:
                for key, value in data.items():
                    setattr(portfolio_image, key, value)
                db.session.commit()
                return jsonify(portfolio_image.to_dict()), 200
            except Exception as e:
                return jsonify({"Error": f"Could not update the profile image {str(e)}"}), 400
        elif request.method == 'DELETE':
            db.session.delete(portfolio_image)
            db.session.commit()
            return jsonify({"Success": "Portfolio image successfully deleted"}), 200

    @app.route('/api/portfolio_images/by_artist/<int:artist_id>', methods=['GET'])
    def handle_portfolio_images_by_artist_id(artist_id):
        portfolio_images = PortfolioImage.query.filter_by(artist_id=artist_id).all()
        portfolio_images_to_dict = [portfolio_image.to_dict() for portfolio_image in portfolio_images]
        return jsonify(portfolio_images_to_dict), 200

    @app.route('/api/services', methods=['GET', 'POST'])
    def handle_services():
        if request.method == 'GET':
            services = Service.query.all()
            services_to_dict = [service.to_dict() for service in services]
            return jsonify(services_to_dict), 200
        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({"Error": "Could not retrieve data"}), 400
            try:
                new_service = Service(**data)
                db.session.add(new_service)
                db.session.commit()
                return jsonify(new_service.to_dict()), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"Error": f"Could not create new service {str(e)}"}), 400

    @app.route('/api/services/<int:service_id>', methods=['GET', 'PUT', 'DELETE'])
    def handle_service(service_id):
        service = Service.query.get_or_404(service_id)
        if request.method == 'GET':
            return jsonify(service.to_dict()), 200
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({"Error": "No Data received"}), 400
            try:
                for key, value in data.items():
                    setattr(service, key, value)
                db.session.commit()
                return jsonify(service.to_dict()), 200
            except Exception as e:
                return jsonify({"Error": f"Could not update the service {str(e)}"}), 400
        elif request.method == 'DELETE':
            db.session.delete(service)
            db.session.commit()
            return jsonify({"Success": "Service successfully deleted"}), 200