from flask import render_template, request, Blueprint, jsonify
from models import Booking, User, Client, Artist, Service, PortfolioImage


def register_routes(app, db):

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/api', methods=['GET'])
    def get_all():
        bookings = Booking.query.all()
        users = User.query.all()
        clients = Client.query.all()
        artists = Artist.query.all()
        services = Service.query.all()
        portfolio_images = PortfolioImage.query.all()
        return render_template(
            'api.html',
            bookings=bookings,
            users=users,
            clients=clients,
            artists=artists,
            services=services,
            portfolio_images=portfolio_images
        )

    @app.route('/api/bookings', methods=['GET'])
    def get_bookings():
        bookings = Booking.query.all()
        return jsonify(bookings)

    @app.route('/api/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify(users)

    @app.route('/api/clients', methods=['GET'])
    def get_clients():
        clients = Client.query.all()
        return jsonify(clients)

    @app.route('/api/artists', methods=['GET'])
    def get_artists():
        artists = Artist.query.all()
        return jsonify(artists)

    @app.route('/api/services', methods=['GET'])
    def get_services():
        services = Service.query.all()
        return jsonify(services)

    @app.route('/api/portfolio-images', methods=['GET'])
    def get_portfolio_images():
        portfolio_images = PortfolioImage.query.all()
        return jsonify(portfolio_images)

