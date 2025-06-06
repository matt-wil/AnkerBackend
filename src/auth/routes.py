from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify
from models import Booking, Client, Artist, Service, PortfolioImage

admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")


def register_admin_routes(app, db):
    app.register_blueprint(admin_blueprint)

    @admin_blueprint.route("/api", methods=["GET"])
    @jwt_required()
    def get_dashboard_data():
        bookings = Booking.query.all()
        clients = Client.query.all()
        artists = Artist.query.all()
        services = Service.query.all()
        portfolio_images = PortfolioImage.query.all()

        return jsonify({
            'bookings': [b.to_dict() for b in bookings],
            'clients': [c.to_dict() for c in clients],
            'artists': [a.to_dict() for a in artists],
            'services': [s.to_dict() for s in services],
            'portfolio_images': [p.to_dict() for p in portfolio_images],
        }), 200

    @admin_blueprint.route("/api/clients", methods=["GET"])
    @jwt_required()
    def search_clients():
        search = request.args.get("search", "")
        clients = Client.query.filter(
            (Client.first_name.ilike(f"%{search}%")) |
            (Client.last_name.ilike(f"%{search}%"))
        ).all()
        return jsonify([client.to_dict() for client in clients]), 200

    @admin_blueprint.route("/api/clients", methods=["POST"])
    @jwt_required()
    def add_client():
        data = request.get_json()
        try:
            new_client = Client(**data)
            db.session.add(new_client)
            db.session.commit()
            return jsonify(new_client.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @admin_blueprint.route('/api/bookings', methods=['GET', 'POST'])
    @jwt_required()
    def handle_bookings():
        if request.method == 'GET':
            bookings = Booking.query.all()
            return jsonify([b.to_dict() for b in bookings]), 200

        elif request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify({"Error": "No Booking Data Found"}), 400
            try:
                new_booking = Booking(**data, created_at=datetime.now())
                db.session.add(new_booking)
                db.session.commit()
                return jsonify(new_booking.to_dict()), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({"Error": f"Could not create item: {str(e)}"}), 400

    @admin_blueprint.route('/api/bookings/<int:booking_id>', methods=['GET', 'PUT', 'DELETE'])
    @jwt_required()
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
                return jsonify(booking.to_dict()), 200
            except Exception as e:
                return jsonify({"Error": f"Could not update the booking: {str(e)}"}), 400
        elif request.method == "DELETE":
            db.session.delete(booking)
            db.session.commit()
            return jsonify({"Success": "Item successfully deleted"}), 200
