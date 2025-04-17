from flask import request, jsonify
from models import Booking, User, Client, Artist, Service, PortfolioImage


def register_routes(app, db):

    @app.route('/', methods=['GET'])
    def index():
        return f"<h1>Welcome to Anker Freiburg Database API<h1>"

    @app.route('/api', methods=['GET'])
    def get_all():
        bookings = Booking.query.all()
        bookings_to_dict = [booking.to_dict() for booking in bookings]
        users = User.query.all()
        users_to_dict = [user.to_dict() for user in users]
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
                'users': users_to_dict,
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
            return jsonify(bookings_to_dict, 200)

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
            return jsonify(booking.to_dict(), 200)
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({"Error": "No data provided"}, 400)
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
            return jsonify({"Message": "Item successfully deleted"}, 200)

    @app.route('/api/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        users_to_dict = [user.to_dict() for user in users]
        return jsonify(users_to_dict, 200)

    @app.route('/api/clients', methods=['GET'])
    def get_clients():
        clients = Client.query.all()
        clients_to_dict = [client.to_dict() for client in clients]
        return jsonify(clients_to_dict, 200)

    @app.route('/api/artists', methods=['GET', 'POST'])
    def handle_artists():
        if request.method == "GET":
            artists = Artist.query.all()
            artists_to_dict = [artist.to_dict() for artist in artists]
            return jsonify(artists_to_dict, 200)

        elif request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"Error": "No Artist Data Found"}, 400)
            try:
                new_artist = Artist(**data)
                db.session.add(new_artist)
                db.session.commit()
                return jsonify(new_artist.to_dict(), 201)
            except Exception as e:
                db.session.rollback()
                return jsonify({"Error": f"Error creating new Artist: {str(e)}"})

    @app.route('/api/artists/<int:artist_id>', methods=["GET", "PUT", "DELETE"])
    def handle_artist(artist_id):
        artist = Artist.query.get_or_404(artist_id)
        if request.method == 'GET':
            return jsonify(artist.to_dict(), 200)
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({"Error": "No Artist data provided"}, 400)
            try:
                for key, value in data.items():
                    setattr(artist, key, value)
                db.session.commit()
                return jsonify(artist.to_dict(), 200)
            except Exception as e:
                return jsonify({"Error": f"Could not update the Artist: {str(e)}"})
        elif request.method == "DELETE":
            db.session.delete(artist)
            db.session.commit()
            return jsonify({"Error": "Item successfully deleted"}, 200)

    @app.route('/api/services', methods=['GET'])
    def get_services():
        services = Service.query.all()
        services_to_dict = [service.to_dict() for service in services]
        return jsonify(services_to_dict, 200)

    @app.route('/api/portfolio-images', methods=['GET'])
    def get_portfolio_images():
        portfolio_images = PortfolioImage.query.all()
        portfolio_images_to_dict = [portfolio_image.to_dict() for portfolio_image in portfolio_images]
        return jsonify(portfolio_images_to_dict, 200)

